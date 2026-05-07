VENV=../Assigments/remitpy3-10/bin/activate

start-backend:
	bash -c "source $(VENV) && cd backend && uvicorn app.main:app --reload"

start-receiver:
	bash -c "cd frontend/receiver_panel/pages/login.html && python3 -m http.server 3000"

start-sender:
	bash -c "cd frontend/sender_panel/pages/login.html && python3 -m http.server 3001"

start-database:
	bash -c "sudo mysql -u root -p"

start-all:
	@echo "Starting backend, receiver, and sender..."
	bash -c "source $(VENV) && cd backend && uvicorn app.main:app --reload & cd frontend/receiver_panel/pages/login.html && python3 -m http.server 3000 & cd frontend/sender_panel/pages/login.html && python3 -m http.server 3001 & wait"

run-tests:
	bash -c "source $(VENV) && export PYTHONPATH=backend && pytest tests/ -v"