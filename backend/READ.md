# BitLoan Backend

## Setup

### 1. Create a virtual environment (if not already done):

**Windows (Command Prompt):**
```
python -m venv .venv
```

**Windows (PowerShell):**
```
python -m venv .venv
```

**macOS/Linux:**
```
python3 -m venv .venv
```

### 2. Activate the virtual environment:

**Windows (Command Prompt):**
```
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```
source .venv/bin/activate
```

**macOS/Linux (Zsh users experiencing compdef errors):**
```
source .venv/bin/activate.zsh
```

### 3. Install dependencies:

```
pip install fastapi uvicorn
```

## Project Structure

The backend is organized as follows:

- **app/**: Main application package
  - **main.py**: Entry point for the FastAPI application
  - **models/**: Database models/schemas (Pydantic models for data validation)
  - **database/**: Database connection and configuration
  - **dependencies/**: Dependency injection components
  - **services/**: Business logic implementation
  - **routers/**: API route definitions
  - **utils/**: Utility functions and helper code
- **main.py**: Root level application entry point
- **.venv/**: Virtual environment (generated when set up)
- **__pycache__/**: Python cache files (automatically generated)

## Running the API

### Start the server:

**Using uvicorn directly (main.py in root):**
```
uvicorn main:app --reload
```

**Using uvicorn with app/main.py:**
```
uvicorn app.main:app --reload
```

**Using the fastapi CLI (if fastapi-cli is installed):**
```
fastapi dev app/main.py
```

**Running the Python script:**
```
python main.py    # Windows
python3 main.py   # macOS/Linux
```

The API will be available at http://localhost:8000

## API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
