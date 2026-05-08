VENV=../Assigments/remitpy3-10/bin/activate

start-backend:
	bash -c "source $(VENV) && cd backend && uvicorn app.main:app --reload"

start-frontend:
	bash -c "cd frontend/ && python3 -m http.server 8001"

start-database:
	bash -c "sudo mysql -u root -p"

start-all:
	@echo "Starting backend and frontend..."
	bash -c "source $(VENV) && cd backend && uvicorn app.main:app --reload & cd frontend && python3 -m http.server 8001 & wait"

run-tests:
	bash -c "source $(VENV) && export PYTHONPATH=backend && pytest tests/ -v"