run:
	@python -m uvicorn main:app --reload 

run-test:
	@python test.py

run-setup:
	@python install -r requirements.txt