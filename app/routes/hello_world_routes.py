from flask import Blueprint

hello_world_bp = Blueprint("hello_world", __name__)

@hello_world_bp.get("/")
def say_hello_world():
    response_body = "Hello, World!"
    return response_body

@hello_world_bp.get("/hello/JSON")
def say_hello_json():
    response_body = {
                        "name": "Kate Belova",
                        "message": "Hello!",
                        "hobbies": ["Fishing", "Swimming", "Collecting Sailor Moon"]
                    }
    return response_body

@hello_world_bp.get("/broken-endpoint-with-broken-server-code")
def broken_endpoint():
    response_body = {
        "name": "Ada Lovelace",
        "message": "Hello!",
        "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
    }
    new_hobby = "Surfing"
    response_body["hobbies"].append(new_hobby)
    return response_body