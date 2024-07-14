// Initialize the map and set default view to Egypt
var map = L.map('map').setView([26.8206, 30.8025], 6);

console.log('Helloooooo')
// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Initialize the sidebar
var sidebar = L.control.sidebar({
    autopan: false,       // whether to maintain the centered map point when opening the sidebar
    closeButton: true,    // whether to add a close button to the panes
    container: 'sidebar', // the DOM container or #ID of a predefined sidebar container that should be used
    position: 'right'     // left or right
}).addTo(map);

// Function to show user's location
function showLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude;
            var lon = position.coords.longitude;
            var userLocation = L.marker([lat, lon]).addTo(map)
                .bindPopup('You are here').openPopup();
            map.setView([lat, lon], 13);
        }, function() {
            alert('Geolocation is not supported by this browser.');
        });
    } else {
        alert('Geolocation is not supported by this browser.');
    }
}




// Function to add markers for each location
function addMarkers() {
    locations.forEach(function(location, index) {
        var locationMarker = L.marker([location.lat, location.long]).addTo(map)
        .bindPopup('name: ' + location.name)
        .openPopup();
        addMarkerToSidebar(location.name, index, locationMarker);
    });
}

// Function to add marker names to sidebar
function addMarkerToSidebar(name, index, marker) {
    var markerList = document.getElementById('marker-list');
    var markerItem = document.createElement('div');
    markerItem.innerHTML = name;
    markerItem.onclick = function() {
        map.setView([locations[index].lat, locations[index].long], 13);
        marker.openPopup();
    };
    markerList.appendChild(markerItem);
}

// Call the addMarkers function to add markers for each location
addMarkers();