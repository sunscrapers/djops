# Djops

Djops is a cookiecutter for Dockerised Django-based projects.

Developed by [SUNSCRAPERS](https://sunscrapers.com/ "SUNSCRAPERS") with 
passion & patience.

## Requirements

To be able to run **djops** you have to have 
[cookiecutter](https://github.com/cookiecutter/cookiecutter) installed:

    pip install cookiecutter

## Quickstart Guide:

To start a new project, do:

    cookiecutter git@github.com:sunscrapers/djops.git

and answer the questions.

This will give you a Docker-Compose project that includes:

* Postgres database;
* Redis;
* Django project;
* Celery worker;
* Celery Beat.

Read the README.md file in your new project directory to learn about how to 
spin your project up, test it, and build it.
