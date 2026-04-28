start-backend:
	bash -c "source ../Assigments/remitpy3-10/bin/activate && cd backend && uvicorn app.main:app --reload"