
compile:
	python -m py_compile *.py

test:
	coverage3 run -m unittest -v tests.test_url
