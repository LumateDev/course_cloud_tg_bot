To run server in dev mode use:

fastapi dev main.py


To run with unicorn:

uvicorn main:app --host 0.0.0.0 --port 8000
