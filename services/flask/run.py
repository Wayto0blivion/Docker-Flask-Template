"""
@author : Zuice
@date : 2024-10-19
"""

from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')