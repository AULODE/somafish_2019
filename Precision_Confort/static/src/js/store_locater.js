

        var position = ["38.885516", "-77.09327200000001"];
        var numDeltas = 100;
        function initialize(position) {
            var latlng = new google.maps.LatLng(position[0], position[1]);
            var myOptions = {
                zoom: 15,
                center: latlng,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                disableDefaultUI: true,
            };
            map = new google.maps.Map(document.getElementById("map"), myOptions);

            marker = new google.maps.Marker({
                position: latlng,
                map: map,
                title: "Latitude:"+position[0]+" | Longitude:"+position[1],
                draggable: true,
            });
        }

        //Load google map
        //google.maps.event.addDomListener(window, 'load', initialize(position));

        function getAddrToLatLong(address){
            //address = "277 Bedford Ave, Brooklyn, NY 11211, USA";
            API_KEY = "AIzaSyAwPAtA1MtShveayE4y8Lb-QYn2DZA-wk4";
            fetch("https://maps.googleapis.com/maps/api/geocode/json?address="+address+'&key='+API_KEY)
            .then(response => response.json())
            .then(data => {
                const latitude = data.results[0].geometry.location.lat;
                const longitude = data.results[0].geometry.location.lng;
                initialize([latitude,longitude]);
            })
        }

        var autocomplete;
        function initAutocomplete() {
            autocomplete = new google.maps.places.Autocomplete(document.getElementById('autocomplete'), {types: ['geocode']});
            initialize(position);
        }