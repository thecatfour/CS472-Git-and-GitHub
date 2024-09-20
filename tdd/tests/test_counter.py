"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

import pytest

from src.counter import app

from src import status


@pytest.fixture()
def client():
    return app.test_client()


@pytest.mark.usefixtures("client")
class TestCounterEndPoints:
    """Test cases for counter-related endpoints"""

    def test_create_a_counter(self, client):
        """It should create a counter"""

        result = client.post("/counters/foo")
        assert result.status_code == status.HTTP_201_CREATED
    
    def test_duplicate_a_counter(self, client):
        """It should return an error for duplicates"""

        result = client.post("/counters/bar")
        assert result.status_code == status.HTTP_201_CREATED

        result = client.post("/counters/bar")
        assert result.status_code == status.HTTP_409_CONFLICT
    
    def test_update_a_counter(self, client):
        """Creates a counter and attempts to increment the counter"""

        result = client.post("/counters/increment_test")

        assert result.status_code == status.HTTP_201_CREATED

        assert result.data == b'{"increment_test":0}\n'

        result = client.put("/counters/increment_test")

        assert result.status_code == status.HTTP_200_OK

        assert result.data == b'{"increment_test":1}\n'

    def test_update_nonexistant_counter(self, client):
        """Attempts to increment a counter that does not exist"""

        result = client.put("/counters/nonexistant_test")

        assert result.status_code == status.HTTP_204_NO_CONTENT
    
    def test_get_counter(self, client):
        """Creates a counter and tries to get the counter without changing it"""

        result = client.post("/counters/get_test")

        assert result.status_code == status.HTTP_201_CREATED

        result = client.get("/counters/get_test")

        assert int(result.data) == 0
        assert result.status_code == status.HTTP_200_OK

        result = client.get("/counters/get_test")

        assert int(result.data) == 0
        assert result.status_code == status.HTTP_200_OK

    def test_get_nonexistant_counter(self, client):
        """Attempts to get a counter that does not exist"""

        result = client.get("/counters/nonexistant_test")

        assert result.status_code == status.HTTP_404_NOT_FOUND