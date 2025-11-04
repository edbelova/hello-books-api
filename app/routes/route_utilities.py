
from ..db import db
from flask import abort, make_response, request

def validate_model(cls, id):
    try:
        id = int(id)
    except:
        handle_error(f"{cls.__name__} {id} invalid", 400)

    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)
    
    if not model:
        handle_error(f"{cls.__name__} {id} not found", 404)
    return model

def handle_error(message, status_code):
    abort(make_response({"message": message}, status_code))

def apply_filtering(query):
    # This function is a placeholder for potential future filtering logic.
    return query

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as error:
        handle_error(f"Invalid request: missing {error.args[0]}", 400)

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201