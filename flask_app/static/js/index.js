var formLogin = document.getElementById('formLogin');
formLogin.onsubmit = function (event) {
    /*"e" es el evento que estoy escuchando (por defecto), quiero prevenir el evento por default de mi formulario*/
    event.preventDefault();
    
    //Obtener los datos del formulario
    var formulario = new FormData(formLogin);
    // formulario = {
    //     "email": "elena@codingdojo.com",
    //     "password": "1234"
    // }

    fetch("/login", { method: 'POST', body:  formulario})
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if(data.message == "correcto") {
                window.location.href = "/dashboard";
            } else {
                var mensajeAlerta = document.getElementById('mensajeAlerta');
                mensajeAlerta.innerHTML = data.message;
                mensajeAlerta.classList.add("alert");
                mensajeAlerta.classList.add("alert-danger");
            }
        });
}