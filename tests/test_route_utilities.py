from app.models.book import Book
from app.routes.route_utilities import validate_model
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
