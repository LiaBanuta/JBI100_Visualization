import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

DATA_PATH = "Australian Shark-Incident Database Public Version.xlsx"

def load_data(file_path):
    data = pd.read_excel(file_path)
    columns_to_keep = [
        'Incident.year', 'Incident.month', 'Victim.injury', 'State', 'Location',
        'Latitude', 'Longitude', 'Site.category', 'Shark.common.name',
        'Provoked/unprovoked', 'Victim.activity'
    ]
    data = data[columns_to_keep]
    data = data.dropna(subset=['Latitude', 'Longitude'])
    data['Latitude'] = pd.to_numeric(data['Latitude'], errors='coerce')
    data['Longitude'] = pd.to_numeric(data['Longitude'], errors='coerce')
    data = data.dropna(subset=['Latitude', 'Longitude'])
    data['Incident.date'] = pd.to_datetime(
        data['Incident.year'].astype(str) + '-' + data['Incident.month'].astype(str),
        errors='coerce'
    )
    data = data.dropna(subset=['Incident.date'])
    return data

shark_data_cleaned = load_data(DATA_PATH)

app = Dash(__name__)
app.title = "Australian Shark Incident Dashboard"

def create_map(data):
    fig = px.scatter_mapbox(
        data,
        lat="Latitude",
        lon="Longitude",
        color="Victim.injury",
        hover_name="Location",
        hover_data={
            "Incident.date": True,
            "Shark.common.name": True,
            "Provoked/unprovoked": True,
            "Victim.activity": True,
        },
        title="Shark Incidents in Australia",
        mapbox_style="carto-positron",
        center={"lat": -25.0, "lon": 135.0},
        zoom=3,
        height=600,
    )
    fig.update_layout(
        title_font=dict(size=20, family="Arial", color="#2C3E50"),
        legend=dict(borderwidth=1, bgcolor="#F4F4F4", bordercolor="#D5D8DC"),
    )
    return fig

def create_bar_chart(data, x_col, title):
    fig = px.bar(
        data,
        x=x_col,
        color="Victim.injury",
        title=title,
        height=400,
        color_discrete_map={"fatal": "#E74C3C", "injured": "#3498DB"}
    )
    fig.update_layout(
        title_font=dict(size=20, family="Arial", color="#2C3E50"),
        plot_bgcolor="#F4F6F7",
        paper_bgcolor="#FDFEFE",
    )
    return fig

app.layout = html.Div(style={'font-family': 'Arial', 'background-color': '#FAFAFA', 'padding': '20px'}, children=[
    html.H1("Australian Shark Incident Dashboard", style={
        'text-align': 'center',
        'color': '#2C3E50',
        'padding-bottom': '20px'
    }),
    html.Div([
        html.Div([
            html.H3("Filters", style={'color': '#2C3E50'}),
            dcc.Dropdown(
                id="injury-filter",
                options=[
                    {"label": "All", "value": "All"},
                    {"label": "Fatal", "value": "fatal"},
                    {"label": "Injured", "value": "injured"},
                ],
                value="All",
                placeholder="Filter by Injury Type",
                style={'margin-bottom': '20px', 'border-radius': '10px', 'padding': '10px'}
            ),
            dcc.Dropdown(
                id="species-filter",
                options=[{"label": s, "value": s} for s in shark_data_cleaned["Shark.common.name"].dropna().unique()],
                placeholder="Filter by Shark Species",
                style={'margin-bottom': '20px', 'border-radius': '10px', 'padding': '10px'}
            ),
            html.Div([
                dcc.Slider(
                    id="year-slider",
                    min=shark_data_cleaned["Incident.date"].dt.year.min(),
                    max=shark_data_cleaned["Incident.date"].dt.year.max(),
                    step=1,
                    value=shark_data_cleaned["Incident.date"].dt.year.min(),
                    marks={
                        year: str(year) for year in range(
                            shark_data_cleaned["Incident.date"].dt.year.min(),
                            shark_data_cleaned["Incident.date"].dt.year.max() + 1, 10
                        )
                    },
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ], style={'padding-top': '20px'}),
        ], style={'width': '25%', 'float': 'left', 'background-color': '#F4F6F7', 'padding': '20px', 'border-radius': '10px'}),
        html.Div([
            html.Div(id="summary-cards", style={
                'display': 'flex',
                'justify-content': 'space-around',
                'padding': '20px',
                'background-color': '#FFFFFF',
                'border-radius': '10px',
                'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.1)',
                'margin-bottom': '20px'
            }),
            dcc.Graph(id="shark-map", style={'border-radius': '10px', 'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.1)'}),
            dcc.Graph(id="analytics-bar", style={'border-radius': '10px', 'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 'margin-top': '20px'}),
        ], style={'width': '70%', 'float': 'right', 'padding': '20px'}),
    ]),
])

@app.callback(
    [Output("shark-map", "figure"),
     Output("analytics-bar", "figure"),
     Output("summary-cards", "children")],
    [Input("injury-filter", "value"),
     Input("species-filter", "value"),
     Input("year-slider", "value")],
)
def update_dashboard(injury_filter, species_filter, year_filter):
    filtered_data = shark_data_cleaned.copy()
    if injury_filter != "All":
        filtered_data = filtered_data[filtered_data["Victim.injury"] == injury_filter]
    if species_filter:
        filtered_data = filtered_data[filtered_data["Shark.common.name"] == species_filter]
    filtered_data = filtered_data[filtered_data["Incident.date"].dt.year == year_filter]

    map_fig = create_map(filtered_data)

    bar_fig = create_bar_chart(filtered_data, x_col="State", title="Incidents by State")

    total_incidents = len(filtered_data)
    fatal_incidents = len(filtered_data[filtered_data["Victim.injury"] == "fatal"])
    unprovoked_incidents = len(filtered_data[filtered_data["Provoked/unprovoked"] == "unprovoked"])

    summary_cards = [
        html.Div(f"Total Incidents: {total_incidents}", style={'border': '1px solid #D5D8DC', 'padding': '10px', 'border-radius': '10px', 'background-color': '#3498DB', 'color': 'white'}),
        html.Div(f"Fatal Incidents: {fatal_incidents}", style={'border': '1px solid #D5D8DC', 'padding': '10px', 'border-radius': '10px', 'background-color': '#E74C3C', 'color': 'white'}),
        html.Div(f"Unprovoked Incidents: {unprovoked_incidents}", style={'border': '1px solid #D5D8DC', 'padding': '10px', 'border-radius': '10px', 'background-color': '#1ABC9C', 'color': 'white'}),
    ]

    return map_fig, bar_fig, summary_cards

if __name__ == "__main__":
    app.run_server(debug=True)
