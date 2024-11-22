To start docker-compose containers:
docker-compose up -d --build

-d runs the containers in the background so that you can continue to use the terminal.
--build updates the containers with whatever changes you have made since the last build.


To stop docker containers:
docker-compose down -v

-v removes any non-persistent containers to free up disk space.

Flask-Migrate will automatically update the database to match the models included in models.py whenever it is launched.

Default login information for 'admin' account can be set in 'services/flask/.env'

Flask project files are in services/flask

To run unit tests:
    From the terminal in the pycharm project, while in the venv, run "pytest". Make sure the docker containers are active.

automation.py can be run manually to perform migrations and unit testing.