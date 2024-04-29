import dash
from dash import html, dcc, callback, Input, Output
import dash_leaflet as dl
from geopy.distance import geodesic
import pandas as pd
import random

dash.register_page(__name__)

# Coordinates for Bologna and random locations in Emilia-Romagna with city names
locations = {
    'Reggio Emilia': (44.7167, 10.6007),  # Province: Reggio Emilia
    'Ferrara': (44.5968, 11.2186),        # Province: Ferrara
    'Cesena': (44.3090, 12.3285)          # Province: Forlì-Cesena
}

# Mock data frame of addresses with assumed coordinates
addresses = pd.DataFrame({
    "Address": ["Via Riva Reno, 23/A", "Via D'Azeglio, 59", "Piazza Maggiore, 5/B",
                "Via Trattati Comunitari Europei 1957-2007, 19", "Via Pirandello, 22/C - Villaggio Pilastro"],
    "Coordinates": [(44.4950, 11.3489), (44.4922, 11.3445), (44.4938, 11.3412),
                    (44.4981, 11.3564), (44.5204, 11.3689)]
})

# Create markers for each location
markers = [dl.Marker(position=coord, title=city) for city, coord in locations.items()]

# Define the map component with the markers
map_component = dl.Map(
    [dl.TileLayer()] + markers,
    style={'width': '100%', 'height': '50vh'},
    center=(44.4949, 11.3426),  # Center on Bologna
    zoom=8
)

# Layout with radio buttons to select a location by city names
layout = html.Div([
    html.H1('Mappa degli utenti non 100% digital'),
    dcc.RadioItems(
        options=[{'label': f'{city} (Coordinates: {coord[0]:.4f}, {coord[1]:.4f})', 'value': city} for city, coord in locations.items()],
        value='Reggio Emilia',
        id='marker-selector'
    ),
    html.Br(),
    map_component,
    html.Br(),
    html.Div(id='closest-location-info')
])

@callback(
    Output('closest-location-info', 'children'),
    Input('marker-selector', 'value')
)
def update_marker_info(selected_city):
    selected_coords = locations[selected_city]
    closest_distance, closest_address = min(
        (geodesic(selected_coords, coord).km, addr) for addr, coord in zip(addresses['Address'], addresses['Coordinates'])
    )

    # Check if filiale scelta distance is greater than the closest distance
    filiale_scelta_distance = random.uniform(10, 100)  # Random mock distance between 10 km and 100 km
    if filiale_scelta_distance > closest_distance:
        return html.P([
            f"La distanza da {selected_city} alla Filiale scelta è {filiale_scelta_distance:.2f} km, "
            f"maggiore della distanza alla filiale più vicina ({closest_distance:.2f} km per {closest_address}). ",
            html.Br(),
            "Gentile Cliente,",
            html.Br(),
            f"Le ricordiamo che la sua filiale più vicina è {closest_address}. Prenoti subito un appuntamento per il contratto di Relax Banking."
        ])
    else:
        return html.P(f"Distanza dalla tua città ({selected_city}) alla filiale più vicina è {closest_distance:.2f} km per {closest_address}.")

