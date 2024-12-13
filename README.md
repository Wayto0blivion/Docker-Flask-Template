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


DOCUMENTATION using SPHINX:
To update the documentation:

From a development environment, cd into the docs folder like this:
cd Docker-Flask-Template\services\flask\docs

Run the following command:
.\make html (Just 'make html' on Linux)

To change what files are included in the documentation, add them here:
services/flask/docs/index.rst

If the configuration needs to be modified, it can be done here:
services/flask/docs/conf.py

More themes for Sphinx can be set in conf.py and can be found here:
https://www.sphinx-doc.org/en/master/usage/theming.html

CRLF line endings for Windows can cause problems with the Flask container not recognizing entrypoint.sh. This can be
fixed by changing line endings to LF.

To add a data-table to an html page, pass the query to it similar to below:
```python
def show_users():
    """
    Shows a list of all users in the system, loaded into a 
    dynamically generated table through data_loader.js.
    Returns:
        Table with all users.
    """
    query_id = str(uuid.uuid4())  # Generate a unique id for each query.
    config = QueryConfiguration(
        id=query_id,
        model_name='user',  # The __tablename__ of the model to user.
        filters={},  # Not filtering the results, so an empty dictionary is passed.
        columns=['id', 'email', 'name'],
        user_id=current_user.id if current_user.is_authenticated else 0
    )
    db.session.add(config)
    db.session.commit()

    return render_template('home.html', title="Users", data_endpoint=f"/api/data?query_id={query_id}")

```


