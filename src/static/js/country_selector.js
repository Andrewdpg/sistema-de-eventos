document.getElementById('paises').addEventListener('change', function() {
    var paisId = this.value;
    fetch('/get_departamentos/?pais_id=' + paisId)
        .then(response => response.json())
        .then(data => {
            var select = document.getElementById('departamentos');
            select.innerHTML = '';

            var option = document.createElement('option');
            option.value = 0;
            option.text = "Departamento";
            select.appendChild(option);
            
            for (var i = 0; i < data.length; i++) {
                option = document.createElement('option');
                option.data = data[i][1];
                option.value = data[i][0];  // codigo
                option.text = data[i][1];  // nombre
                select.appendChild(option);
            }
        });
});

document.getElementById('departamentos').addEventListener('change', function() {
    var dptoId = this.value;
    fetch('/get_ciudades/?dpto_id=' + dptoId)
        .then(response => response.json())
        .then(data => {
            var select = document.getElementById('ciudades');
            select.innerHTML = '';

            var option = document.createElement('option');
            option.value = 0;
            option.text = "Ciudad";
            select.appendChild(option);
            
            for (var i = 0; i < data.length; i++) {
                option = document.createElement('option');
                option.data = data[i][1];
                option.value = data[i][0];  // codigo
                option.text = data[i][1];  // nombre
                select.appendChild(option);
            }
        });
});