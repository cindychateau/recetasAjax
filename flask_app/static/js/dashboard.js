var btnSw = document.getElementById('sw');
btnSw.onclick = function(e) {
    e.preventDefault();

    fetch("https://swapi.dev/api/people", {method: 'GET'})
        .then( response => response.json() )
        .then( data => {
            var p = '';
            lista_personajes = data.results
            for(var i = 0; i< lista_personajes.length; i++) {
                p +="<p>"+lista_personajes[i].name+"</p>";
            }

            document.getElementById('divSw').innerHTML = p;

        })

}