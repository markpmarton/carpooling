"""
Basic acceptance test.
"""

import json

from .test_base import client


def test_acceptance():
    # Accepts valid PUT cars request
    data = [{"id": 1, "seats": 5}, {"id": 2, "seats": 4}, {"id": 3, "seats": 6}]
    resp = client.put("/cars", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 200
    # Accepts valid POST journey request
    data = {"id": 1, "people": 4}
    resp = client.post(
        "/journey", data=json.dumps(data), content_type="application/json"
    )
    assert resp.status_code == 200
    # Accepts valid POST locate request
    data = {"ID": 1}
    resp = client.post(
        "/locate", data=data, content_type="application/x-www-form-urlencoded"
    )
    assert resp.status_code == 200
    # Returns valid payload for POST locate request
    # assert resp.json == {"id": 2, "max_seats": 4, "free_seats": 0}
    assert resp.json == {"id": 2, "seats": 4}
    # Accepts valid POST dropoff request
    data = {"ID": 1}
    resp = client.post(
        "/dropoff", data=data, content_type="application/x-www-form-urlencoded"
    )
    assert resp.status_code == 200
