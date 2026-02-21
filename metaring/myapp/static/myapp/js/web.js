document.addEventListener("DOMContentLoaded", function () {
    
    const form = document.getElementById("airport-search-form");
    const input = document.getElementById("icao_input");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        let icao = input.value.trim().toUpperCase();

        if (icao.length === 4) {
            window.location.href = "/airport/" + icao + "/";
        } else {
            alert("ICAO must be 4 letters.");
        }
    });

});