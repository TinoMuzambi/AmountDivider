import math

import pytest

from app import app, divide_amount


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    return app.test_client()


def test_home_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Amount Divider" in response.data


def test_valid_submission_displays_partitions(client):
    response = client.post("/", data={"amount": "100", "partitions": "3"})

    assert response.status_code == 200
    assert b"Partition 1" in response.data
    assert b"Partition 3" in response.data


@pytest.mark.parametrize("partitions", ["0", "-1", "1001"])
def test_invalid_partition_count_is_rejected(client, partitions):
    response = client.post("/", data={"amount": "100", "partitions": partitions})

    assert response.status_code == 200
    assert b"Partitions must be between 1 and 1,000" in response.data
    assert b"Partition 1 -" not in response.data


def test_division_is_descending_and_preserves_total():
    partitions = divide_amount(123.45, 8)

    assert partitions == sorted(partitions, reverse=True)
    assert math.isclose(sum(partitions), 123.45, rel_tol=0, abs_tol=1e-9)


@pytest.mark.parametrize("amount, partitions", [(0, 1), (-1, 1), (10, 0)])
def test_division_rejects_invalid_arguments(amount, partitions):
    with pytest.raises(ValueError):
        divide_amount(amount, partitions)
