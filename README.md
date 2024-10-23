
# Tech stack

- Python+poetry+Flask
- HTMX
- SQLite

# How to run

You can see it in action on [fly.io](https://secret-santa.fly.dev/).
To run it locally, you need to have [poetry](https://python-poetry.org/) installed, and then run:
- `poetry install`
- `poetry shell`
- `flask db upgrade`  (to create a sqlite database)

and finally run with `flask run --debug` and check [localhost:5000](http://localhost:5000/)

# Decisions

To do the task in the suggested maximum time I had to cut things like:
- tests
- a responsive UI
- error handling

Instead I made sure the minimum features were working, and I invested a bit more time in making it deployable on fly.io.

All the code is a single file, since it was simple enough and didn't really make sense to split at this point.
