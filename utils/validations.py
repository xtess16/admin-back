import re


# Валидация UUID. Должен быть в таком формате 0290707f-527d-46d4-a86b-2842b31a7d01
def validate_uuid4(uuid_string):
    return re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$', uuid_string)
