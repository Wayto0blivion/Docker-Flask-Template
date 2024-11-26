"""
@author : Zuicie
@date : 2024-10-19

The entrypoint for starting the flask application. Ignores setting the app variable if Sphinx is building documentation.
"""

import os
from website import create_app


# Avoid setting app here if this is building documentation through Sphinx. Instead, app will be set in docs/conf.py.
if os.getenv("SPHINX_BUILD") == '1':
    app = None
else:
    # Set the app variable during normal operation.
    app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')