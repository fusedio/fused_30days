# Contributed by Marko Letic https://www.linkedin.com/in/marko-letic/

import streamlit as st

st.set_page_config(page_title="Fused 30 Days #7: Vintage Map", page_icon="⚪️")
st.sidebar.header("Day 7 - Vintage Map")

# Display title and subtitle information
st.title("Frodo and Sam's Journey")

st.write("""
In this interactive visualization, follow Frodo and Sam's journey through Middle-earth as they traverse various landscapes.
""")

# HTML and JavaScript for the DeckGL map with animation
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="initial-scale=1, maximum-scale=1, user-scalable=no" />
    <title>DeckGL Animated Path</title>
    <style>
        body { margin: 0; }
        #map { width: 100%; height: 100vh; }
        #fullscreenBtn {
            position: absolute;
            top: 10px;
            right: 10px;
            z-index: 10;
            padding: 10px 15px;
            background-color: rgba(0, 0, 0, 0.5);
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
    <script src="https://unpkg.com/deck.gl@latest/dist.min.js"></script>
</head>
<body>
    <button id="fullscreenBtn">Fullscreen</button>
    <div id="map"></div>
    <script>
        const { DeckGL, TripsLayer, TerrainLayer } = deck;

        const initialViewState = {
            longitude: -1.4157,
            latitude: 52.2324,
            zoom: 6,
            pitch: 40.5,
            bearing: 0,
        };

        async function fetchPathData(url) {
            const response = await fetch(url);
            const data = await response.json();
            return data;
        }

        function createGeoPathWithTimestamps(path) {
            return path.map((coords, index) => ({
                coordinates: [coords[0], coords[1]], 
                timestamp: index,
            }));
        }

        const elevationDataUrl = "https://i.imgur.com/OaEPJWM.png";

        async function initMap() {
            const newPathData = await fetchPathData("https://gist.githubusercontent.com/mletic/a202956add25cc02763b2f52561b7f0b/raw/d0eead8bd21df5478024c113cd25b6a88aa9de5c/lotr-path-elevated.json");
            const frodoSamGeoPathWithTimestamps = createGeoPathWithTimestamps(newPathData);

            const terrainLayer = new TerrainLayer({
                id: "terrain-layer",
                elevationData: elevationDataUrl,
                texture: "https://i.imgur.com/Jp46N2Q.jpeg",
                bounds: [-2, 51, 0, 53],
                elevationDecoder: {
                    rScaler: 10,
                    gScaler: 0.1,
                    bScaler: 0.05,
                    offset: 0,
                },
                meshMaxError: 100,
                material: { diffuse: 1 },
            });

            const tripLayer = new TripsLayer({
                id: "trip-layer",
                data: [{
                    path: newPathData,
                    timestamps: frodoSamGeoPathWithTimestamps.map(d => d.timestamp),
                    color: [0, 0, 255],
                }],
                getPath: (d) => d.path,
                getTimestamps: (d) => d.timestamps,
                getColor: (d) => d.color,
                trailLength: 100,
                widthMinPixels: 4,
                currentTime: 0,
            });

            const deckgl = new DeckGL({
                container: "map",
                initialViewState,
                controller: true,
                layers: [terrainLayer, tripLayer],
            });

            let currentTime = 0;

            function animate() {
                currentTime = (currentTime + 0.15) % frodoSamGeoPathWithTimestamps.length;
                deckgl.setProps({
                    layers: [
                        new TripsLayer({
                            id: "trip-layer",
                            data: [{
                                path: newPathData,
                                timestamps: frodoSamGeoPathWithTimestamps.map(d => d.timestamp),
                                color: [0, 0, 255],
                            }],
                            getPath: (d) => d.path,
                            getTimestamps: (d) => d.timestamps,
                            getColor: (d) => d.color,
                            trailLength: 100,
                            widthMinPixels: 4,
                            currentTime,
                        }),
                        terrainLayer,
                    ],
                });
                requestAnimationFrame(animate);
            }
            animate();
        }

        // Fullscreen functionality
        document.getElementById('fullscreenBtn').addEventListener('click', function() {
            const mapContainer = document.getElementById('map');
            if (mapContainer.requestFullscreen) {
                mapContainer.requestFullscreen();
            } else if (mapContainer.mozRequestFullScreen) { // Firefox
                mapContainer.mozRequestFullScreen();
            } else if (mapContainer.webkitRequestFullscreen) { // Chrome, Safari and Opera
                mapContainer.webkitRequestFullscreen();
            } else if (mapContainer.msRequestFullscreen) { // IE/Edge
                mapContainer.msRequestFullscreen();
            }
        });

        initMap();
    </script>
</body>
</html>
"""

# Create an iframe to display the HTML code
st.components.v1.html(html_code, height=600, scrolling=True)