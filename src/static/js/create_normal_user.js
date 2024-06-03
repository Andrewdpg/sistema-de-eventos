function submitForm() {
    var formData = new FormData();

    let identificacion = document.getElementById("identificacion").value;
    let email = document.getElementById("email").value;
    let nombres = document.getElementById("nombres").value;
    let apellidos = document.getElementById("apellidos").value;
    let nombre_usuario = document.getElementById("nombre_usuario").value;
    let password1 = document.getElementById("password1").value;
    let password2 = document.getElementById("password2").value;

    let tipo_relacion = document.getElementById("tipo_relacion").value;

    let ciudad = {
        "nombre": document.getElementById("ciudades").options[document.getElementById("ciudades").selectedIndex].text,
        "departamento": document.getElementById("departamentos").options[document.getElementById("departamentos").selectedIndex].text,
        "pais": document.getElementById("paises").options[document.getElementById("paises").selectedIndex].text
    };

    formData.append('identificacion', identificacion);
    formData.append('email', email);
    formData.append('nombres', nombres);
    formData.append('apellidos', apellidos);
    formData.append('nombre_usuario', nombre_usuario);
    formData.append('password1', password1);
    formData.append('password2', password2);
    formData.append('tipo_relacion', tipo_relacion);
    formData.append('ciudad', JSON.stringify(ciudad));

    fetch('/create_normal_user/', {
        method: 'POST',
        body: JSON.stringify(Object.fromEntries(formData.entries())),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        // Redirige a otra página
        window.location.href = "/";
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
