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

### 3. Install dependencies:

```
pip install fastapi uvicorn
```

## Running the API

### Start the server:

**Using uvicorn directly:**
```
uvicorn main:app --reload
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
