var listCategoryItems = [];
var listFacilitadores = [];
var listConferencistas = [];
var listFacultadesOrg = [];

function addCategory() {
    var input = document.getElementById("categoria").value;
    listCategoryItems.push(input);
    var li = document.createElement("li");
    li.appendChild(document.createTextNode(input));
    document.getElementById("categoriaList").appendChild(li);
    document.getElementById("categoria").value = "";
}

function addEnabler() {
    var input = document.getElementById("facilitadores").value;
    listFacilitadores.push(input);
    var li = document.createElement("li");
    li.appendChild(document.createTextNode(input));
    document.getElementById("facilitadoresList").appendChild(li);
    document.getElementById("facilitadores").value = "";
}

function addOrganizer() {
    var input = document.getElementById("facultades").value; 
    
    if (input != "none") {
        listFacultadesOrg.push(input);
        var     li = document.createElement("li");
        li.appendChild(document.createTextNode(input));
        document.getElementById("facultadOrgList").appendChild(li);
    }
}

function submitForm() {
    var formData = new FormData();

    let titulo = document.getElementById("titulo").value;
    let descripcion = document.getElementById("descripcion").value;
    let fecha = document.getElementById("fecha").value;
    
    let lugar = [
        document.getElementById("nombre_lugar").value,
        document.getElementById("direccion_lugar").value
    ];

    let paises = document.getElementById("paises");
    let departamentos = document.getElementById("departamentos");
    let ciudades = document.getElementById("ciudades");

    let ubicacion = [
        paises.options[paises.selectedIndex].text,
        departamentos.options[departamentos.selectedIndex].text,
        ciudades.options[ciudades.selectedIndex].text
    ];

    lugar.push(ubicacion);

    let programa_org = document.getElementById("programa_org").value;

    formData.append('titulo', titulo);
    formData.append('descripcion', descripcion);
    formData.append('fecha', fecha);
    formData.append('lugar', JSON.stringify(lugar));
    formData.append('categorias', JSON.stringify(listCategoryItems));
    formData.append('conferencistas', JSON.stringify(listConferencistas));
    formData.append('facilitadores', JSON.stringify(listFacilitadores));   
    formData.append('facultades_org', JSON.stringify(listFacultadesOrg));   
    formData.append('programa_org', programa_org);

    fetch('/create_event/', {
        method: 'POST',
        body: JSON.stringify(Object.fromEntries(formData.entries())),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => console.log(data))
    .catch((error) => {
        console.error('Error:', error);
    });

    print(titulo);
}

// TODO: cambiar el event a 'input' pero revisar que tenga delay, porque si digitas rapido no se logra borrar la lista, asi que salen resultados repetidos
// TODO: mejorar la query, lo que pasas es que si digita "123" quiero que la cedula sea "123..." y no "...123..." lo mismo para el nombre, de igual forma acepta los "espacios, por lo tanto si borras todo, el query devuelve todos los resultados"
document.getElementById('conferencistas').addEventListener('change', function() {
    document.getElementById("conferencistasSearchList").innerHTML = '';

    var conferSearch = this.value;
    fetch('/get_conferencistas/?confer_search=' + conferSearch)
        .then(response => response.json())
        .then(data => {
            for (var i = 0; i < data.length; i++) { 
                var li = document.createElement("li");
                li.id = data[i]['identificacion'];
                li.appendChild(document.createTextNode(data[i]['identificacion'] + ' | ' + data[i]['nombres'] + ' ' + data[i]['apellidos']));

                li.addEventListener('click', function() {
                    var newLi = this.cloneNode(true);
                    listConferencistas.push(this.id);
                    // TODO: no puede agregar los mismos conferencistas
                    document.getElementById("conferencistasList").appendChild(newLi);
                });

                document.getElementById("conferencistasSearchList").appendChild(li);     
            }
        });
});