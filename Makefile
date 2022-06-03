LOCAL_DB_PATH = local.db

.PHONY: all 
all: populate_new_db run_server

# Create a new SQLite database locally and populate the new database. 
# If there is an existing database, delete the old one.
populate_new_db:
ifneq ("$(wildcard $(LOCAL_DB_PATH))","")
	rm -f $(LOCAL_DB_PATH)
endif
	
	python -c "from app.data_processing.main import create_and_populate_db; create_and_populate_db()"

# Start the FastAPI server
run_server:
	uvicorn app.simple_api.main:app