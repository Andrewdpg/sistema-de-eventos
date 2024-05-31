def document_employee(nombre_usuario, password, identificacion):
    employee = {
        "last_login": None,
        "identificacion": identificacion,
        "nombre_usuario": nombre_usuario,
        "password": password,
        "is_superuser": False,
    }

    return employee