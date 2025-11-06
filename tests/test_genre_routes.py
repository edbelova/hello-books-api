def test_get_all_genres_with_no_records(client):
    # Act
    response = client.get("/genres")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_genres_with_two_records(client, two_saved_genres):
    # Act
    response = client.get("/genres")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 1,
        "name": "Fantasy"
    }
    assert response_body[1] == {
        "id": 2,
        "name": "Science Fiction"
    }

def test_get_all_genres_with_name_filter(client, two_saved_genres):
    # Act
    response = client.get("/genres?name=Fantasy")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0] == {
        "id": 1,
        "name": "Fantasy"
    }

def test_get_all_genres_with_no_matching_filter(client, two_saved_genres):
    # Act
    response = client.get("/genres?name=Nonexistent")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_create_one_genre(client):
    # Arrange
    new_genre = {
        "name": "Mystery"
    }

    # Act
    response = client.post("/genres", json=new_genre)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "Mystery"
    }

def test_create_genre_no_name(client):
    # Arrange
    new_genre = {
        # "name" is missing
    }

    # Act
    response = client.post("/genres", json=new_genre)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "message": "Invalid request: missing name"
    }

    def test_create_genre_empty_name(client):
        # Arrange
        new_genre = {
            "name": ""
        }

        # Act
        response = client.post("/genres", json=new_genre)
        response_body = response.get_json()

        # Assert
        assert response.status_code == 201
        assert response_body == {
            "id": 1,
            "name": ""
        }

    def test_create_genre_with_extra_keys(client):
        # Arrange
        new_genre = {
            "name": "Horror",
            "description": "Scary books"
        }

        # Act
        response = client.post("/genres", json=new_genre)
        response_body = response.get_json()

        # Assert
        assert response.status_code == 201
        assert response_body == {
            "id": 1,
            "name": "Horror"
        }