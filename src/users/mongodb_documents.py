def document_employee(nombre_usuario, password, identificacion):
    employee = {
        "last_login": None,
        "identificacion": identificacion,
        "nombre_usuario": nombre_usuario,
        "password": password,
        "is_superuser": False,
    }

    return employee

def document_user(identificacion, nombre_usuario, password, nombres, apellidos, tipo_empleado, email, pais, departamento, ciudad):
    user = {
        "last_login": None,
        "identificacion": identificacion,
        "nombre_usuario": nombre_usuario,
        "password": password,
        "is_superuser": False,
        "nombres": nombres,
        "apellidos": apellidos,
        "tipo_empleado": tipo_empleado,
        "email": email,
        "pais": pais,
        "departamento": departamento,
        "ciudad": ciudad,
    }

    return user