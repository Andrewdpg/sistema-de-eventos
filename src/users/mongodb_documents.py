def document_employee(nombre_usuario, password, identificacion):
    employee = {
        "password": password,
        "last_login": None,
        "identificacion": identificacion,
        "nombre_usuario": nombre_usuario,
        "is_superuser": False,
    }

    return employee

def document_base_user(nombre_usuario, password, identificacion, is_superuser=False):
    base_user = {
        "password": password,
        "last_login": None,
        "identificacion": identificacion,
        "nombre_usuario": nombre_usuario,
        "is_superuser": is_superuser,
    }

    return base_user