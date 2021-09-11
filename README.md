# Django Exam Organization Tool

A tool to organize exam tasks seperately and join them into an exam.

## Language

The default language is german. You have to change several entries in different files.

## Requirements

This app uses Django as well as several django-modules, listed in requirements.txt. To install all required modules use `pip install -r requirements.txt`.

Also you need to have LaTeX installed on your system, e. g. [TeXLive](https://www.tug.org/texlive/).

Last you need to set up a `.env` file with at least a SECRET_KEY variable in the root folder.

## Change LaTeX-Output

To change LaTeX output edit "exam.tex" in "exam_organization/templates/latex". There you'll also find several configuration files. Feel free to use your own preamble.

## Development server

After installing all dependencies run `python manage.py runserver` to run the app in a development server. Visit `localhost:8000` to view the app.

In this mode the app uses an sqlite3-database.

## Production server
 
 The app uses [PostgreSQL](https://www.postgresql.org/) in production. Create a database and add the credentials to your `.env` file. Use the following variable names:

POSTGRES_DB_NAME, POSTGRES_DB_USER, POSTGRES_DB_PASSWORD

Afterwards type `python manage.py runserver --settings=exam_organization_tool.settings.production` to run the production server locally. For deployment use other environments like docker, heroku or gunicorn.

## Improvements

If you have any idea for improvements feel free to create an issue.

