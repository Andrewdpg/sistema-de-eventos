def evento(data):
    """
    Create a MongoDB document based on the input data.
    :param data_to_parse: dictionary with the input data
    :return: dictionary representing a MongoDB document
    """

    event_document = {
        "titulo": data['titulo'],
        "img_url": data['img_url'],
        "descripcion": data['descripcion'],
        "categorias": data['categorias'],
        "fecha": data['fecha'],
        "lugar": data['lugar'],
        "conferencistas": data['conferencistas'],
        "facilitadores": data['facilitadores'],
        "organizadores": data['organizadores'], 
    }

    return event_document