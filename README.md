# Back-end Application
This demo back-end application consists of two services, data processing service and API service. 

## Prerequisites

[Python 3.10](https://www.python.org/downloads/)

[make](https://www.gnu.org/software/make/)

## Quickstart
- (Optional) Set up virtual environment  
  - Create a virtual environment, `python -m venv ign`
  	- Note: the virtual environment will be installed in current folder.
  - Activate virtual environment for Linux, `source ign/bin/activate`
    - For other OS, check out [link](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)
  - Deactivate virtual environment, `deactivate`
  - Delete the virtual environment, `rm -rf ign`
- Install dependencies, run `pip install -r requirements.txt`
	- Note: you can verify this step by running `pytest`
- (Optional) Modify development environment variables in `.env.dev`
- Create and populate database, run `make populate_new_db`
- Start API server, run `make run_server`

## Run Test
- Tests for this application are located in `tests/` folder
- (Optional) Modify variables are defined in `.env.test`
- Run all tests, run `pytest`
- Run a specific test, run `pytest tests/folder/filename.py::testname`
    - For example, `pytest tests/simple_db/test_crud.py::test_review_get_by_id`

## Data Processing Service
[Link](./app/data_processing/README.md)

## API Service
[Link](./app/simple_api/README.md)

## Roadmap
1. change synchronous database operation to asynchronous.
2. add proper cache mechanism. Current cache mechanism caches returned response as a whole, which could be a list, therefore, not very efficient. What's more, current design assumes no update on database.
3. more comprehensive error handling on query.
4. add logger.
5. add functionality to update/insert new record to database, and dynamically reflect the new updates on the cache (or just mark the old data in cache as dirty and out-of-date). 
6. add more test cases.
