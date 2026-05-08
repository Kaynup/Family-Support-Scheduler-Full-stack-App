VENV=../Assigments/remitpy3-10/bin/activate

start-backend:
	bash -c "source $(VENV) && cd backend && uvicorn app.main:app --reload"

start-frontend:
	bash -c "cd frontend/ && python3 ../scripts/start_frontend.py"

start-database:
	bash -c "sudo mysql -u root -p"

start-all:
	@echo "Starting backend and frontend..."
	bash -c "source $(VENV) && cd backend && uvicorn app.main:app --reload & cd frontend && python3 ../scripts/start_frontend.py & wait"

run-tests:
	bash -c "source $(VENV) && export PYTHONPATH=backend && pytest tests/ -v"