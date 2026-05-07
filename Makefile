VENV=/home/remitpe/MAIN/Assigments/remitpy3-10/bin/activate

start-backend:
	bash -c "source $(VENV) && cd backend && uvicorn app.main:app --reload"

start-receiver:
	bash -c "cd frontend/receiver_panel && python -m http.server 3000"

start-sender:
	bash -c "cd frontend/sender_panel && python -m http.server 3001"

start-database:
	bash -c "sudo mysql -u root -p"

run-tests:
	bash -c "source $(VENV) && pytest tests/ -v"