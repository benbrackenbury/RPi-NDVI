clean:
	rm -rf __pycache__ ./src/__pycache__ ./src/lib/__pycache__
	rm -rf build dist *.spec

setup:
	pip3 install -Ur requirements.txt

preview:
	python3 src/preview.py

webview:
	python3 src/webview.py