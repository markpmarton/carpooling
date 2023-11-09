"""
Tests covering most of the edge cases for the API.

I ran the tests locally with a virtual envirnment
with the following command:

python -m pytest
"""

import pytest
from random import randint
from .test_base import client


def test_status():
    response = client.get("/status")
    assert response.status_code == 200


def test_car_registration_valid_input():
    response = client.put("/cars", json=[{"id": randint(1, 100000), "seats": 4}])
    assert response.status_code == 200


def test_car_registration_missing_id():
    response = client.put("/cars", json=[{"seats": 4}])
    assert response.status_code == 400


def test_car_registration_missing_seats():
    response = client.put("/cars", json=[{"id": randint(1, 100000)}])
    assert response.status_code == 400


def test_car_registration_invalid_type_id():
    response = client.put(
        "/cars", json=[{"id": f"{str(randint(1,100000))}", "seats": 4}]
    )
    assert response.status_code == 400


def test_car_registration_invalid_type_seats():
    response = client.put("/cars", json=[{"id": randint(1, 100000), "seats": "4"}])
    assert response.status_code == 400


def test_car_registration_invalid_seat_number1():
    response = client.put("/cars", json=[{"id": randint(1, 100000), "seats": 1}])
    assert response.status_code == 400


def test_car_registration_invalid_seat_number3():
    response = client.put("/cars", json=[{"id": randint(1, 100000), "seats": 3}])
    assert response.status_code == 400


def test_car_registration_invalid_seat_number10():
    response = client.put("/cars", json=[{"id": randint(1, 100000), "seats": 10}])
    assert response.status_code == 400


def test_car_registration_unexpected_parameter():
    response = client.put(
        "/cars", json=[{"id": f"{str(randint(1,100000))}", "seats": 4, "unexpected": 2}]
    )
    assert response.status_code == 400


def test_car_registration_empty_list():
    response = client.put("/cars", json=[])
    assert response.status_code == 400


def test_journey_registration_valid_input():
    response = client.post("/journey", json={"id": randint(1, 100000), "people": 6})
    assert response.status_code == 200


def test_journey_registration_missing_id():
    response = client.post("/journey", json={"people": 6})
    assert response.status_code == 400


def test_journey_registration_missing_people():
    response = client.post("/journey", json={"id": randint(1, 100000)})
    assert response.status_code == 400


def test_journey_registration_invalid_type_id():
    response = client.post(
        "/journey", json={"id": f"{str(randint(1,100000))}", "people": 6}
    )
    assert response.status_code == 400


def test_journey_registration_invalid_type_people():
    response = client.post("/journey", json={"id": randint(1, 100000), "people": "6"})
    assert response.status_code == 400


def test_journey_registration_invalid_unexpected_parameter():
    response = client.post(
        "/journey", json={"id": randint(1, 100000), "people": 6, "unexpected": 2}
    )
    assert response.status_code == 400


def test_dropoff_valid_input():
    journey_id = randint(1, 100000)
    client.post("/journey", json={"id": journey_id, "people": 6})
    response = client.post("/dropoff", data={"ID": f"{journey_id}"})
    assert response.status_code == 200


def test_dropoff_missing_id():
    response = client.post("/dropoff", content_type="application/x-www-form-urlencoded")
    assert response.status_code == 400


def test_dropoff_no_id_found():
    response = client.post("/dropoff", data={"NO_ID": "100001"})
    assert response.status_code == 400


def test_dropoff_no_journey_found():
    response = client.post("/dropoff", data={"ID": "100001"})
    assert response.status_code == 404


def test_locate_existing_journey_with_car():
    journey_id = randint(1, 100000)
    car_id = randint(1, 100000)
    client.post("/journey", json={"id": journey_id, "people": 1})
    client.put("/cars", json=[{"id": car_id, "seats": 6}])
    response = client.post("/locate", data={"ID": f"{journey_id}"})
    assert response.status_code == 200
    assert response.json["id"] > 0


def test_locate_existing_journey_no_car():
    journey_id = randint(1, 100000)
    for _ in range(10):
        client.post("/journey", json={"id": randint(1, 100000), "people": 6})

    client.post("/journey", json={"id": journey_id, "people": 6})
    response = client.post("/locate", data={"ID": f"{journey_id}"})
    assert not response.json
    assert response.status_code == 204


def test_locate_missing_id():
    response = client.post("/locate", data={"NO_ID": "100002"})
    assert response.status_code == 400


def test_locate_missing_journey():
    response = client.post("/locate", data={"ID": "1"})
    assert response.status_code == 404
