"""
Starting point of the application.
Creates the Flask service and serves it with the waitress
server.

Start server: python main.py
"""

from waitress import serve
from api.app import get_app


def run_app(app):
    return serve(app, host=app.config["HOST"], port=app.config["PORT"])


if __name__ == "__main__":
    app = get_app()
    run_app(app)
