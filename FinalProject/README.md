# Dosa Restaurant Backend API

This project is a backend API using FastAPI to handle orders in restaurant

## Requirements

- Python 3.7+
- FastAPI
- SQLite
- Pydantic

## Setup

1. Clone this repository.
2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Initialize the database:

    ```bash
    python db_setup.py
    ```

4. Populate the database with data:

    ```bash
    python insert_db.py
    ```

5. Run the FastAPI app:

    ```bash
    uvicorn main:app --reload
    ```

    The API will be available at `http://127.0.0.1:8000`.


