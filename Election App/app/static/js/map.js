/* global L */

let map;

export function initMap() {
    map = L.map('map').setView([52.233, 21.006], 12);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
}

export function updateMap(data) {
    const lat = parseFloat(data.lat);
    const lon = parseFloat(data.lon);
    const bounds = [
        [parseFloat(data.bounds[0]), parseFloat(data.bounds[2])],
        [parseFloat(data.bounds[1]), parseFloat(data.bounds[3])]
    ];
    const geojson = data.geojson;

    removeAllMarkers();
    removeGeoJSONLayers();
    
    if(!geojson)
        placeMarker(lat, lon)

    const zoom = map.getBoundsZoom(bounds);
    
    L.geoJSON(data.geojson, {
        style: {
            color: '#007bff',
            weight: 2,
            fillOpacity: 0.1
        }
    }).addTo(map)

    map.flyTo([lat, lon], zoom, {
        duration: 3
    });
}

function placeMarker(lat, lon) {
    L.marker([lat, lon]).addTo(map);
}

function removeAllMarkers() {
    map.eachLayer(function (layer) {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });
}

function removeGeoJSONLayers() {
    map.eachLayer(function (layer) {
        if (layer instanceof L.GeoJSON) {
            map.removeLayer(layer);
        }
    });
}

/*
    enable/disable drag and zoom while in flyTo animation
*/