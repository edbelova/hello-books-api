from app.models.genre import Genre
import pytest

def test_from_dict_returns_genre():
    # Arrange
    genre_data = {
        "name": "Mystery"
    }

    # Act
    new_genre = Genre.from_dict(genre_data)

    # Assert
    assert new_genre.name == "Mystery"

def test_from_dict_with_no_name():
    # Arrange
    genre_data = {
    }

    # Act & Assert
    with pytest.raises(KeyError, match = 'name'):
        new_genre = Genre.from_dict(genre_data)

def test_from_dict_with_extra_keys():
    # Arrange
    genre_data = {
        "extra": "some stuff",
        "name": "Horror",
        "another": "last value"
    }

    # Act
    new_genre = Genre.from_dict(genre_data) 

    # Assert
    assert new_genre.name == "Horror"

def test_to_dict_no_missing_data():
    # Arrange
    test_data = Genre(id = 1,
                      name="Romance")
    
    # Act
    genre_dict = test_data.to_dict()

    # Assert
    assert genre_dict["id"] == 1
    assert genre_dict["name"] == "Romance"

def test_to_dict_missing_id():
    # Arrange
    test_data = Genre(name="Thriller")

    # Act
    result = test_data.to_dict()

    # Assert
    assert result["id"] is None

def test_to_dict_missing_name():
    # Arrange
    test_data = Genre(id=2)

    # Act
    result = test_data.to_dict()

    # Assert
    assert result["name"] is None