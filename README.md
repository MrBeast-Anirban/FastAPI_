# FastAPI_

A modern, fast (high-performance) web API built using **FastAPI** and Python. This project is structured to provide clean, scalable endpoints with automatic data validation and interactive documentation.

---

## 🚀 Features

* **High Performance**: Built on top of Starlette and Pydantic, matching the speed of NodeJS and Go.
* **Automatic Documentation**: Interactive API documentation generated automatically via Swagger UI and ReDoc.
* **Data Validation**: Robust data serialization and type validation using Pydantic.
* **Environment Setup**: Fully compatible with isolated Python virtual environments.

---

## 🛠️ Getting Started

Follow these steps to set up the repository locally on your machine.

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### 2. Clone the Repository
```bash
git clone git@github-mrbeast:MrBeast-Anirban/FastAPI_.git
cd FastAPI_
```

### 3. Set Up the Virtual Environment
Create and activate your Python virtual environment (e.g., `myenv`):
```bash
# Create the environment
python3 -m venv myenv

# Activate the environment (macOS/Linux)
source myenv/bin/activate
```

### 4. Install Dependencies
Make sure you have your requirements file ready, or manually install the core dependencies:
```bash
pip install --upgrade pip
pip install fastapi uvicorn
# Or if you have a requirements.txt file:
# pip install -r requirements.txt
```

---

## 💻 Running the Application

Start the local development server using **Uvicorn**:

```bash
uvicorn main:app --reload
```
*Note: Replace `main` with your entrypoint file name if your main file is named differently (e.g., `app:app`).*

Once the server starts, you can access the application at:
* **Base URL**: `http://127.0.0.1:8000`

---

## 📖 API Documentation

FastAPI automatically provisions interactive UI suites to test your endpoints:

* **Swagger UI (Interactive Docs)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc (Alternative Docs)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 📚 Detailed Module & Folder Breakdown

This project is structured sequentially. As the prefix number increases, the complexity and production-readiness of the code increase.

### 📄 File-by-File Demonstrations

* **`01_hello_world.py`**
  * **Demonstrates**: The bare minimum setup required to spin up a FastAPI instance.
  * **Core Concepts**: Instantiating `FastAPI()`, creating basic route decorators (`@app.get("/")`), returning native Python dictionaries as automated JSON responses, and setting up the Uvicorn gateway.

* **`02_path_parameters.py`**
  * **Demonstrates**: How to capture dynamic values straight out of the URL path string.
  * **Core Concepts**: Using curly braces in path configurations (`/items/{item_id}`), enforcing strict data types (e.g., forcing an ID to be an `int`), and analyzing the automated `422 Unprocessable Entity` error when the wrong data type is provided.

* **`03_query_parameters.py`**
  * **Demonstrates**: Handling optional, non-path variables passed via query strings (e.g., `?skip=0&limit=10`).
  * **Core Concepts**: Defining default fallback parameters, managing optional query fields via Python's `Optional` or `None` syntax, and combining path parameters with query parameters in a single function signature.

* **`04_request_body.py`**
  * **Demonstrates**: Receiving and parsing structured data incoming from incoming client client payloads (like a JSON payload from a frontend form).
  * **Core Concepts**: Creating schema definitions using **Pydantic models**, handling incoming data objects, type safety checks, and auto-generating request schemas within the documentation.

* **`05_validation.py`**
  * **Demonstrates**: Advanced structural boundaries and validation constraints for incoming parameters.
  * **Core Concepts**: Implementing `Query` and `Path` classes to enforce length limits (`min_length`, `max_length`), numeric boundaries (`gt`, `le`), regex patterns, and adding customized descriptive metadata to the Swagger UI.

* **`06_crud_operations.py`**
  * **Demonstrates**: Combining all prior concepts to build a fully operational mock REST API.
  * **Core Concepts**: Implementing complete **C**reate, **R**ead, **U**pdate, and **D**elete cycles, manipulating an in-memory database dictionary, and handling standard functional status returns (like raising a `404 Not Found` exception via `HTTPException`).

---

### 📂 Folder Structure Demonstrations

If your repository transitions from single flat files into a multi-file architecture, the folders demonstrate these design patterns:

* **`app/` or `src/`**
  * **Demonstrates**: Production-grade structural isolation. Instead of writing all code in one massive file, this folder structures modules logically by responsibility.
  
* **`routers/` / `api/`**
  * **Demonstrates**: Distributed routing using **`APIRouter`**. This isolates endpoints by resource domain (e.g., `users.py`, `products.py`) and mounts them seamlessly back to the centralized core file.

* **`models/` / `schemas/`**
  * **Demonstrates**: Separation of data shapes. 
    * `schemas/` houses Pydantic models handling data input/output contracts.
    * `models/` houses the database blueprints (e.g., SQLAlchemy ORM models).

* **`core/` / `config/`**
  * **Demonstrates**: Global environment management. Uses `pydantic-settings` to securely ingest `.env` configuration keys, set cross-origin parameters (CORS), and manage global project values.

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
