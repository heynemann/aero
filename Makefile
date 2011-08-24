test:
	@PYTHONPATH=$$PYTHONPATH:. pyvows vows/

ci:
	@PYTHONPATH=$PYTHONPATH:. pyvows --cover --cover_package=aero --cover_threshold=80.0 -r aero.coverage.xml -x vows/

setup:
	@pip install -r requirements.txt
	@pip install -r test_requirements.txt
