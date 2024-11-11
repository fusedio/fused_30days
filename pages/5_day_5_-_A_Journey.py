# Contributed by Marko Letic https://www.linkedin.com/in/marko-letic/

import streamlit as st

st.set_page_config(page_title="Fused 30 Days #5: A Journey", page_icon="⚪️")
st.sidebar.header("Day 5 - A Journey")

# Display title and subtitle information
st.title("British Trans-Arctic Expedition")

st.write("""
From 1968 to 1969, Sir Wally Herbert led the British Trans-Arctic Expedition, a 3,800-mile overland crossing of the Arctic Ocean, from Alaska to Spitsbergen, which some historians had billed as "the last great journey on Earth." 
""")

# HTML and JavaScript for the ArcGIS map with refined animation, tooltips, and modal
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="initial-scale=1, maximum-scale=1, user-scalable=no" />
    <title>Animated Arctic Expedition Path with Modal Info</title>
    <link rel="stylesheet" href="https://js.arcgis.com/4.30/esri/themes/dark/main.css" />
    <style>
        html, body, #viewDiv { padding: 0; margin: 0; height: 100%; width: 100%; background-color: black; }
        /* Modal styling */
        #infoModal {
            position: absolute;
            top: 20px;
            right: 20px;
            background-color: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 15px;
            border-radius: 8px;
            width: 300px;
            display: none;
            font-family: Arial, sans-serif;
            font-size: 14px;
        }
        #infoModal.show {
            display: block;
        }
        #infoModal h3 {
            margin-top: 0;
            font-size: 16px;
        }
    </style>
    <script src="https://js.arcgis.com/4.30/"></script>
    <script>
        let animationInterval;
        let animationIndex = 0;

        // Waypoint data with additional details
        const waypoints = [
            { date: "February 21, 1968", location_name: "Point Barrow, Alaska", coordinates: [-156.7887, 71.2906], descriptions: ["The expedition departs with four members: Wally Herbert (leader), Allan Gill (navigator), Roy 'Fritz' Koerner (glaciologist), and Dr. Kenneth Hedges (surgeon and photographer).", "The team uses traditional Inuit-style dog sleds to traverse the ice, beginning their journey across the frozen Arctic Ocean."] },
            { date: "March 1968", location_name: "Central Arctic Ocean", coordinates: [-150.0, 85.0], descriptions: ["Temperature ranges from -45°F to -50°F (-43°C to -46°C).", "The team faces intense cold, slow progress due to rough ice, and limited daylight.", "They encounter early hardships adapting to Arctic conditions."] },
            { date: "April 1968", location_name: "Central Arctic Ocean", coordinates: [-150.0, 86.0], descriptions: ["The team moves steadily over shifting ice floes, facing difficult navigation and constant re-adjustment of direction.", "The expedition is resupplied by air, providing essential food and fuel."] },
            { date: "May 1968", location_name: "Central Arctic Ocean", coordinates: [-150.0, 87.0], descriptions: ["Significant delays occur due to drifting ice pushing them southward, reversing some of their progress.", "Frustration builds, and the team must adapt constantly to maintain a northward path."] },
            { date: "Summer 1968", location_name: "Central Arctic Ocean", coordinates: [-150.0, 88.0], descriptions: ["The Arctic sun remains above the horizon, but melting ice forms dangerous leads of open water.", "A series of supply drops provides essential provisions despite the logistical challenges posed by the moving ice.", "The team travels about 10 miles a day."] },
            { date: "Fall 1968", location_name: "Central Arctic Ocean", coordinates: [-150.0, 89.0], descriptions: ["With decreasing daylight, temperatures drop and ice becomes thicker and more stable.", "The team battles constant darkness and extreme cold, relying on careful rationing to survive."] },
            { date: "February 1969", location_name: "Central Arctic Ocean", coordinates: [-150.0, 89.5], descriptions: ["The team marks one year since leaving Alaska, noting both their progress and the physical and psychological toll.", "They rely heavily on each other and their dogs for warmth and companionship."] },
            { date: "March 1969", location_name: "Near the North Pole", coordinates: [0.0, 89.9], descriptions: ["The team is close to the North Pole, facing worsening ice conditions but maintaining motivation to reach their goal.", "Despite exhaustion, they press onward."] },
            { date: "April 6, 1969", location_name: "The North Pole", coordinates: [0.0, 90.0], descriptions: ["The team reaches the North Pole, becoming the first to do so by surface travel.", "They confirm their position through celestial navigation, achieving a monumental milestone in Arctic exploration."] },
            { date: "May 29, 1969", location_name: "Spitsbergen, Svalbard, Norway", coordinates: [16.0, 78.0], descriptions: ["The expedition completes the first-ever surface crossing of the Arctic Ocean, reaching Spitsbergen in Svalbard, Norway.", "They covered approximately 4,000 miles over 16 months, achieving a historic feat in polar exploration."] }
        ];

        require([
            "esri/Map", "esri/layers/GraphicsLayer", "esri/views/MapView", 
            "esri/Graphic", "esri/geometry/Polyline", "esri/widgets/Expand", "esri/layers/TileLayer"
        ], function(Map, GraphicsLayer, MapView, Graphic, Polyline, Expand, TileLayer) {
            const pathLayer = new GraphicsLayer();
            const tooltipLayer = new GraphicsLayer();
            let currentPath = [];

            function updateModal(content) {
                const modal = document.getElementById("infoModal");
                modal.innerHTML = content;
                modal.classList.add("show");
            }

            function animatePath() {
                if (animationIndex < waypoints.length) {
                    const currentWaypoint = waypoints[animationIndex];
                    currentPath.push(currentWaypoint.coordinates);

                    const line = new Polyline({
                        paths: [currentPath],
                        spatialReference: { wkid: 4326 }
                    });

                    const lineGraphic = new Graphic({
                        geometry: line,
                        symbol: {
                            type: "simple-line",
                            color: [253, 128, 93, 0.8],
                            width: 3
                        }
                    });

                    pathLayer.removeAll();
                    pathLayer.add(lineGraphic);

                    // Restore the circle marker for the current waypoint
                    const pointGraphic = new Graphic({
                        geometry: {
                            type: "point",
                            longitude: currentWaypoint.coordinates[0],
                            latitude: currentWaypoint.coordinates[1]
                        },
                        symbol: {
                            type: "simple-marker",
                            color: [255, 255, 255, 0.8],
                            size: 8,
                            outline: { color: [253, 128, 93, 0.8], width: 1 }
                        },
                        popupTemplate: {
                            title: "Expedition Event",
                            content: currentWaypoint.location_name
                        }
                    });

                    tooltipLayer.add(pointGraphic);

                    // Update the modal with current waypoint info
                    const descriptionList = currentWaypoint.descriptions.map(desc => `<li>${desc}</li>`).join("");
                    const modalContent = `<h3>${currentWaypoint.location_name}</h3><p><strong>Date:</strong> ${currentWaypoint.date}</p><ul>${descriptionList}</ul>`;
                    updateModal(modalContent);

                    animationIndex++;
                } else {
                    animationIndex = 0;
                    currentPath = [];
                    tooltipLayer.removeAll();
                }
            }

            setInterval(animatePath, 3000); // Call the animation function every 3 seconds

            const arcticBaseLayer = new TileLayer({
                url: "https://services.arcgisonline.com/arcgis/rest/services/Polar/Arctic_Ocean_Base/MapServer"
            });

            const map = new Map({
                basemap: {
                    baseLayers: [arcticBaseLayer]
                },
                layers: [pathLayer, tooltipLayer]
            });

            const view = new MapView({
                container: "viewDiv",
                map: map,
                center: [0, 90],
                zoom: 3,
                popup: { dockEnabled: true, dockOptions: { breakpoint: false } }
            });

        });
    </script>
</head>
<body>
    <div id="viewDiv"></div>
    <div id="infoModal" class="modal"></div>
</body>
</html>
"""


st.components.v1.html(html_code, height=600, scrolling=True)