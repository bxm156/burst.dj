from sqlalchemy.types import TypeDecorator, TEXT
import simplejson

class JSONValue(TypeDecorator):
    "Represents an immutable container as a json-encoded string."

    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = simplejson.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = simplejson.loads(value)
        return value