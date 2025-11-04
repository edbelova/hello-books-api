from app.models.book import Book
from app.models.author import Author
from app.routes.route_utilities import validate_model
from app.routes.route_utilities import create_model
import pytest
from werkzeug.exceptions import HTTPException

def test_validate_model(two_saved_books):
    # Act
    result_model = validate_model(Book, 1)

    # Assert
    assert result_model.id == 1
    assert result_model.title == "Ocean Book"
    assert result_model.description == "watr 4evr"

def test_validate_model_missing_record(two_saved_books):
    # Act & Assert
    with pytest.raises(HTTPException):
        result_model = validate_model(Book, "3")

def test_validate_model_invalid_id(two_saved_books):
    # Act & Assert
    with pytest.raises(HTTPException):
        result_model = validate_model(Book, "cat")

def test_create_model_book(client):
    # Arrange
    test_data = {
        "title": "New Book",
        "description": "The Best!"
    }

    # Act
    result = create_model(Book, test_data)

    # Assert
    assert isinstance(result, tuple)
    assert result[0]["id"] == 1
    assert result[0]["title"] == "New Book"
    assert result[0]["description"] == "The Best!"
    assert result[1] == 201


def test_create_model_book_missing_data(client):
    # Arrange
    test_data = {
        "description": "The Best!"
    }

    # Act & Assert
    with pytest.raises(HTTPException) as error:
        result_book = create_model(Book, test_data)

    response = error.value.response
    assert response.status == "400 BAD REQUEST"

def test_create_model_author(client):
    # Arrange
    test_data = {
        "name": "New Author"
    }

    # Act
    result = create_model(Author, test_data)

    # Assert
    assert isinstance(result, tuple)
    assert result[0]["id"] == 1
    assert result[0]["name"] == "New Author"
    assert result[1] == 201