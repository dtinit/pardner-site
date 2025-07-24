# pardner-site

## Setup
To run locally, first install dependencies with pip:

```bash
python -m pip install -r requirements.txt
```

Then, initialize the local database:

```bash
python manage.py migrate
```

Finally, start the local development server:

```bash
python manage.py runserver
```

## Administration
To access the admin site, create a superuser account:

```bash
python manage.py createsuperuser
```

Then visit /admin and log in with your credentials.
