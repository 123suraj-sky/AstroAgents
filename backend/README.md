# AstroAgents Backend

The backend is a FastAPI application. Its Python project configuration is defined in `pyproject.toml`.

## `pyproject.toml`

`pyproject.toml` declares:

- The project name and version.
- The minimum supported Python version (`3.10` or newer).
- FastAPI as the web framework.
- Uvicorn as the development server.
- Setuptools as the build and installation backend.

The dependency declarations in `pyproject.toml` mean that a separate `requirements.txt` file is not required for this project.

## Set Up The Virtual Environment

From PowerShell, run these commands from the `backend` directory:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

The virtual environment keeps backend packages isolated from the system Python installation. It is recommended even though dependencies are declared in `pyproject.toml`.

If PowerShell blocks activation scripts for the current session, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## Run The API

Make sure the terminal's current directory is `backend`, the virtual environment is active, and the dependencies are installed:

```powershell
uvicorn app.main:app --reload
```

The API is then available at:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

The `app.main:app` value means:

- `app.main` is the `main.py` module inside the `app` package.
- `app` is the FastAPI application object defined in that module.

Run the command from `backend` so Python can resolve the `app` package correctly.

## Generated Files

Running `python -m pip install -e .` may create `astroagents_backend.egg-info/`. This is generated setuptools metadata containing package and dependency information. It is not source code and should not be committed to GitHub.

The repository ignores it with:

```text
*.egg-info/
```

The same applies to virtual environments and Python bytecode such as `.venv/`, `__pycache__/`, and `*.pyc` files.

## Updating Dependencies

Add or change runtime dependencies in `pyproject.toml`, then reinstall the project from the `backend` directory:

```powershell
python -m pip install -e .
```

A `requirements.txt` file is only needed if the project later adopts a workflow that specifically requires one, such as legacy deployment tooling or separately pinned exported dependencies.
