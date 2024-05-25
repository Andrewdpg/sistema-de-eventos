def employee_doc(nombre_usuario, password, identificacion):
    employee = {
        "last_login": None,
        "identificacion": identificacion,
        "nombre_usuario": nombre_usuario,
        "password": password,
        "is_superuser": False,
    }

    return employee

def user_doc(identificacion, nombre_usuario, password, nombres, apellidos, tipo_empleado, email, pais, departamento, ciudad):
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

def evento_doc(titulo, descripcion, categorias, fecha, lugar_datos, conferencistas, facilitadores, facultades_org, programa_org, img_url=None):
    """
    Create a MongoDB document based on the input data.
    :param data_to_parse: dictionary with the input data
    :return: dictionary representing a MongoDB document
    """

    event_document = {
        "titulo": titulo,
        "descripcion": descripcion,
        "categorias": categorias,
        "fecha": fecha,
        "conferencistas": conferencistas,
        "facilitadores": facilitadores,
        "facultades_org": facultades_org,
    }

    lugar = {
        "nombre" : lugar_datos[0],
        "direccion" : lugar_datos[1],
    }

    ciudad_datos = {
        "nombre": lugar_datos[2][0],
        "departamento": lugar_datos[2][1],
        "pais": lugar_datos[2][2],
    }    

    lugar["ciudad"] = ciudad_datos
    event_document["lugar"] = lugar

    if programa_org is not None:
            event_document["programa_org"] = programa_org  

    if img_url is not None:
        event_document["img_url"] = img_url

    return event_document