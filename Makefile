start-backend:
	bash -c "source ../Assigments/remitpy3-10/bin/activate && cd backend && uvicorn app.main:app --reload"
start-frontend:
	bash -c "source ../Assigments/remitpy3-10/bin/activate && cd frontend && python -m http.server 8080"
start-database:
	bash -c "sudo mysql -u root -p"