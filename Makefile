test:
	@PYTHONPATH=$$PYTHONPATH:. pyvows vows/

setup:
	@pip install -r requirements.txt
	@pip install -r test_requirements.txt
