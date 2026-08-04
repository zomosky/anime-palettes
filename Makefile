# 重新生成整个色库。改了 src/data.py 里的配色后跑 `make all`。
PY ?= python3
SRC := src
OUT := dist

.PHONY: all tune derive py html files pptx docs test clean

all: derive py html files pptx docs test

## 1. 科研可用性微调（约 40s，结果写进 src/tuned.py）
tune:
	cd $(SRC) && $(PY) tune.py

## 2. 派生深浅变体、四种色标、色环数据、色盲评级 -> src/library.json
derive:
	cd $(SRC) && $(PY) derive.py

## 3. 生成可 import 的 Python 模块
py: derive
	cd $(SRC) && $(PY) gen_py.py && mv build/anime_palettes.py ../anime_palettes.py

## 4. 单文件交互色卡库
html: derive
	cd $(SRC) && $(PY) gen_html.py && mv build/anime-palettes.html ../$(OUT)/

## 5. csv / xlsx / ase / gpl / ppt 主题色 / origin 清单
##    先删后拷：光靠 cp 覆盖的话，改名或删掉一套配色之后，dist/ 里的旧色板文件
##    会一直留着；CI 只 diff 那几个确定性文件，抓不到这种孤儿产物。
##    另外逐项拷贝而不是 `cp -r build/*`，免得 build/ 里的中间文件被顺手带进 dist/。
files: derive
	cd $(SRC) && $(PY) gen_files.py
	rm -rf $(OUT)/ase $(OUT)/gpl $(OUT)/ppt-theme-colors $(OUT)/origin-hex
	cp -r $(SRC)/build/ase $(SRC)/build/gpl $(SRC)/build/ppt-theme-colors \
	      $(SRC)/build/origin-hex $(OUT)/
	cp $(SRC)/build/anime_palettes.csv $(SRC)/build/anime_palettes.json \
	   $(SRC)/build/anime_palettes.xlsx $(OUT)/

## 6. PPT 取色板（需要 node + pptxgenjs）
pptx: derive
	cd $(SRC) && node gen_pptx.js && mv build/anime-palettes-picker.pptx ../$(OUT)/

## 7. 文档配图
docs: derive
	cd $(SRC) && $(PY) sheet2.py && mv build/配色总览.png ../docs/images/
	$(PY) -c "import matplotlib;matplotlib.use('Agg');import anime_palettes as ap;\
ap.wheel_all(save='docs/images/色环总览.png');\
ap.scatter_guide('ganyu',save='docs/images/散点配色策略.png')"

test:
	$(PY) -m pytest tests/ -q

clean:
	rm -rf $(SRC)/build $(SRC)/__pycache__ __pycache__ .pytest_cache

## 8. 打包 Claude Skill（速查表从 library.json 重新生成）
##    先 rm 再打：zip 对已存在的包是增量更新，删掉 references 里的文件后重打包，
##    旧条目仍留在 .skill 里 —— CI 的 diff -r 会报错，而 make skill 修不好它。
skill:
	$(PY) src/gen_skill_table.py
	rm -f skills/anime-palettes.skill
	cd skills && zip -qr anime-palettes.skill anime-palettes -x '*.DS_Store' && echo "wrote skills/anime-palettes.skill"
