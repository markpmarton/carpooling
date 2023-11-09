"""
Environment setup for testing.
"""

import pytest
from multiprocessing import Process

from api.app import get_app

app = get_app()
client = app.test_client()


@pytest.fixture
def run_api_server():
    app.config.update(
        {
            "TESTING": True,
        }
    )

    server_process = Process(
        target=app.run(host=app.config["HOST"], port=app.config["PORT"], debug=True),
        args=(app,),
    )
    server_process.start()

    yield

    server_process.terminate()
    server_process.join()
