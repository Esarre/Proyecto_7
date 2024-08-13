/* Código que permite listar comunas en base a la región seleccionada*/

document.addEventListener('DOMContentLoaded', function() {
    const regionField = document.getElementById('id_region');
    const comunaField = document.getElementById('id_comuna');

    if (regionField) {
        regionField.addEventListener('change', function() {
            const regionId = this.value;
            fetch(`/obtener_comunas/?region_id=${regionId}`)
                .then(response => response.json())
                .then(data => {
                    comunaField.innerHTML = '<option value="">---------</option>';
                    data.forEach(comuna => {
                        const option = document.createElement('option');
                        option.value = comuna.id;
                        option.textContent = comuna.comuna;
                        comunaField.appendChild(option);
                    });
                });
        });
    }
});