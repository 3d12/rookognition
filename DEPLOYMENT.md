# Deployment

1. Prepare deployment package:
  - Update pyproject.toml to new version
  - Squash feature branch commits into new version
  - Apply tag and commit
  - Build wheel file
    - To build wheel file:
      > python -m build
2. Transfer deployment package to deployment environment
3. SSH into deployment environment
4. Create virtual environment
    > python3 -m venv .venv
5. Activate virtual environment
    > . .venv/bin/activate
6. Use pip to install (e.g. for v0.0.1)
    > pip install rookognition-0.0.1-py3-none-any.whl
  - If this is an upgrade, use pip uninstall to remove the old version first
  - This will install all runtime dependencies of the package as well
7. Generate a new secret key for config.py
    > echo "SECRET_KEY = '$(python -c "import secrets; print(secrets.token_hex())")'" > ./.venv/var/rookognition-instance/config.py
8. Install WSGI interface (e.g. waitress) if not already installed
    > pip install waitress
9. Use WSGI interface to serve the app
    > waitress-serve --call 'rookognition:create_app'
10. Configure nginx if not already configured
  - Ensure that listening on port 80/443 is redirected to port 8080 internally
