 Session-based authentication
- Simple HTML UI
- Basic validation and error handling
- Clean app package structure
- Auto-created SQLite schema

## Project Structure

|   |   `-- register.html
|   |-- __init__.py
|   |-- db.py
|   `-- routes.py
|   |-- routes.py
|   `-- schema.sql
|-- .gitignore
|-- README.md
|-- requirements.txt

- The SQLite database file is created automatically at `instance/users.db`.
- To use a stronger session secret, set the `SECRET_KEY` environment variable before starting the app.
- Session cookies are configured as `HttpOnly` and `SameSite=Lax`.

## Optional: Set a Custom Secret Key

PowerShell:

```powershell
$env:SECRET_KEY = "your-very-strong-secret-key"
python run.py
```

## If `python` Does Not Work on Windows

Some Windows systems only have the Microsoft Store alias enabled. In that case:

1. Install Python from the official installer.
2. During installation, check `Add python.exe to PATH`.
3. Reopen PowerShell and run:

   ```powershell
   python --version
   ```

4. Then repeat the setup steps above.