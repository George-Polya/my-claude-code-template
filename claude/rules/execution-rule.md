# Execution Rule

## Python Environment
- All Python work must use the project's `.venv` virtual environment
- Use `.venv/bin/python3` to run Python
- Use `.venv/bin/pytest` for Python tests

```bash
source .venv/bin/activate        # activate before any Python command
pip install -r requirements.txt  # install inside venv, never globally
```

- If `.venv` does not exist, request it from the user
