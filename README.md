# Inventory Project (Django)

Minimal inventory management app built with Django.

## Features
- Categories and products CRUD
- Search and category filter
- Low stock and stock value stats
- Per-device data isolation using a browser cookie key

## Local Setup
```bash
cd inventory_project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
## Railway
Use start command:
```bash
python inventory_project/manage.py migrate --noinput && python inventory_project/manage.py collectstatic --noinput && gunicorn inventory_project.wsgi --chdir inventory_project --bind 0.0.0.0:$PORT --workers 2
```
