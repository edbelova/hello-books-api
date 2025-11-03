import pytest

def test_get_all_authors_with_no_records(client):
    # Act
    response = client.get("/authors")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_authors_with_two_records(client, two_saved_authors):
    # Act
    response = client.get("/authors")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 1,
        "name": "Author One"
    }
    assert response_body[1] == {
        "id": 2,
        "name": "Author Two"
    }

def test_get_all_authors_with_name_query_matching_none(client, two_saved_authors):
    # Act
    data = {'name': 'Desert Author'}
    response = client.get("/authors", query_string=data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_authors_with_name_query_matching_one(client, two_saved_authors):
    # Act
    data = {'name': 'Author One'}
    response = client.get("/authors", query_string=data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0] == {
        "id": 1,
        "name": "Author One"
    }

def test_get_one_author(client, two_saved_authors):
    # Act
    response = client.get("/authors/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Author One"
    }

def test_get_one_author_missing_record(client, two_saved_authors):
    # Act
    response = client.get("/authors/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Author 3 not found"}

def test_get_one_author_invalid_id(client, two_saved_authors):
    # Act
    response = client.get("/authors/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Author cat invalid"}

def test_create_one_author(client):
    # Act
    response = client.post("/authors", json={
        "name": "New Author"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "New Author"
    }

def test_create_one_author_no_name(client):
    # Arrange
    test_data = {}

    # Act
    response = client.post("/authors", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {'message': 'Invalid request: missing name'}

def test_create_one_author_with_extra_keys(client):
    # Arrange
    test_data = {
        "name": "New Author",
        "bio": "The Best!"
    }

    # Act
    response = client.post("/authors", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "New Author",
    }

def test_update_one_author(client, two_saved_authors):
    # Arrange
    test_data = {
        "name": "Updated Author"
    }
    
    # Act
    response = client.put("/authors/1", json=test_data)

    # Assert
    assert response.status_code == 200
    assert response.get_json() == {
        "id": 1,
        "name": "Updated Author"
    }

def test_update_author_with_extra_keys(client, two_saved_authors):
    # Arrange
    test_data = {
        "name": "New Author",
        "bio": "The Best!"
    }

    # Act
    response = client.put("/authors/1", json=test_data)

    # Assert
    assert response.status_code == 200
    assert response.get_json() == {
        "id": 1,
        "name": "New Author"
    }

def test_update_author_missing_record(client, two_saved_authors):
    # Arrange
    test_data = {
        "name": "New Author",
        "bio": "The Best!"
    }

    # Act
    response = client.put("/authors/3", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Author 3 not found"}

def test_update_author_invalid_id(client, two_saved_authors):
    # Arrange
    test_data = {
        "name": "New Author",
        "bio": "The Best!"
    }

    # Act
    response = client.put("/authors/cat", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Author cat invalid"}

def test_delete_author(client, two_saved_authors):
    # Act
    response = client.delete("/authors/1")

    # Assert
    assert response.status_code == 204
    assert response.content_length is None

def test_delete_author_missing_record(client, two_saved_authors):
    # Act
    response = client.delete("/authors/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Author 3 not found"}

def test_delete_author_invalid_id(client, two_saved_authors):
    # Act
    response = client.delete("/authors/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Author cat invalid"}