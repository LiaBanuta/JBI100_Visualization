import pandas as pd
from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

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

# Custom CSS for better styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
        <style>
            * { font-family: 'Roboto', sans-serif; }
            .card {
                transition: all 0.3s ease;
                cursor: pointer;
            }
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 15px rgba(0,0,0,0.2);
            }
            .filter-container {
                backdrop-filter: blur(10px);
                background-color: rgba(255,255,255,0.9);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


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
        color_discrete_map={"fatal": "#E74C3C", "injured": "#3498DB"},
    )
    fig.update_layout(
        title_font=dict(size=24, family="Roboto", color="#2C3E50"),
        legend=dict(
            borderwidth=1,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#D5D8DC",
            font=dict(size=12, family="Roboto"),
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_trend_chart(data):
    yearly_data = data.groupby([data['Incident.date'].dt.year, 'Victim.injury']).size().reset_index()
    yearly_data.columns = ['Year', 'Injury', 'Count']

    fig = px.line(
        yearly_data,
        x='Year',
        y='Count',
        color='Injury',
        title="Incident Trends Over Time",
        color_discrete_map={"fatal": "#E74C3C", "injured": "#3498DB"},
    )
    fig.update_layout(
        title_font=dict(size=20, family="Roboto", color="#2C3E50"),
        plot_bgcolor="rgba(255,255,255,0.9)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Year",
        yaxis_title="Number of Incidents",
        hovermode="x unified",
    )
    return fig


def create_activity_chart(data):
    activity_data = data.groupby(['Victim.activity', 'Victim.injury']).size().reset_index()
    activity_data.columns = ['Activity', 'Injury', 'Count']

    fig = px.bar(
        activity_data,
        x='Activity',
        y='Count',
        color='Injury',
        title="Incidents by Victim Activity",
        color_discrete_map={"fatal": "#E74C3C", "injured": "#3498DB"},
    )
    fig.update_layout(
        title_font=dict(size=20, family="Roboto", color="#2C3E50"),
        plot_bgcolor="rgba(255,255,255,0.9)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Activity",
        yaxis_title="Number of Incidents",
        xaxis_tickangle=-45,
    )
    return fig


app.layout = html.Div(style={
    'background-color': '#F0F2F5',
    'min-height': '100vh',
    'padding': '20px'
}, children=[
    html.Div([
        html.H1("Australian Shark Incident Dashboard", style={
            'text-align': 'center',
            'color': '#2C3E50',
            'font-weight': '700',
            'margin-bottom': '30px',
            'font-size': '36px'
        }),

        # Filters Panel
        html.Div([
            html.Div([
                html.H3("Filters", style={'color': '#2C3E50', 'margin-bottom': '20px'}),
                dcc.Dropdown(
                    id="injury-filter",
                    options=[
                        {"label": "All Incidents", "value": "All"},
                        {"label": "Fatal Incidents", "value": "fatal"},
                        {"label": "Non-fatal Injuries", "value": "injured"},
                    ],
                    value="All",
                    className="filter-dropdown",
                    style={'margin-bottom': '20px'}
                ),
                dcc.Dropdown(
                    id="species-filter",
                    options=[{"label": s, "value": s} for s in
                             shark_data_cleaned["Shark.common.name"].dropna().unique()],
                    placeholder="Select Shark Species",
                    className="filter-dropdown",
                    style={'margin-bottom': '20px'}
                ),
                html.Div([
                    html.Label("Select Year Range:", style={'margin-bottom': '10px'}),
                    dcc.RangeSlider(
                        id="year-range-slider",
                        min=shark_data_cleaned["Incident.date"].dt.year.min(),
                        max=shark_data_cleaned["Incident.date"].dt.year.max(),
                        step=1,
                        value=[
                            shark_data_cleaned["Incident.date"].dt.year.min(),
                            shark_data_cleaned["Incident.date"].dt.year.max()
                        ],
                        marks={
                            year: str(year) for year in range(
                                shark_data_cleaned["Incident.date"].dt.year.min(),
                                shark_data_cleaned["Incident.date"].dt.year.max() + 1,
                                10
                            )
                        },
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                ], style={'padding-top': '20px'}),
            ], className="filter-container", style={
                'padding': '25px',
                'border-radius': '15px',
                'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'margin-bottom': '20px'
            }),
        ], style={'width': '25%', 'float': 'left'}),

        # Main Content
        html.Div([
            # Summary Cards
            html.Div(id="summary-cards", style={
                'display': 'flex',
                'justify-content': 'space-between',
                'margin-bottom': '20px',
                'gap': '15px'
            }),

            # Interactive Map
            html.Div([
                dcc.Graph(id="shark-map")
            ], style={
                'background-color': 'white',
                'padding': '20px',
                'border-radius': '15px',
                'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'margin-bottom': '20px'
            }),

            # Analytics Section
            html.Div([
                html.Div([
                    dcc.Graph(id="trend-chart", style={'height': '400px'})
                ], style={'width': '50%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(id="activity-chart", style={'height': '400px'})
                ], style={'width': '50%', 'display': 'inline-block'}),
            ], style={
                'background-color': 'white',
                'padding': '20px',
                'border-radius': '15px',
                'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'display': 'flex'
            }),
        ], style={'width': '73%', 'float': 'right'}),
    ], style={'max-width': '1800px', 'margin': '0 auto'}),
])


@app.callback(
    [Output("shark-map", "figure"),
     Output("trend-chart", "figure"),
     Output("activity-chart", "figure"),
     Output("summary-cards", "children")],
    [Input("injury-filter", "value"),
     Input("species-filter", "value"),
     Input("year-range-slider", "value")],
)
def update_dashboard(injury_filter, species_filter, year_range):
    filtered_data = shark_data_cleaned.copy()

    # Apply filters
    if injury_filter != "All":
        filtered_data = filtered_data[filtered_data["Victim.injury"] == injury_filter]
    if species_filter:
        filtered_data = filtered_data[filtered_data["Shark.common.name"] == species_filter]

    filtered_data = filtered_data[
        (filtered_data["Incident.date"].dt.year >= year_range[0]) &
        (filtered_data["Incident.date"].dt.year <= year_range[1])
        ]

    # Create visualizations
    map_fig = create_map(filtered_data)
    trend_fig = create_trend_chart(filtered_data)
    activity_fig = create_activity_chart(filtered_data)

    # Create summary cards with more detailed statistics
    total_incidents = len(filtered_data)
    fatal_incidents = len(filtered_data[filtered_data["Victim.injury"] == "fatal"])
    unprovoked_incidents = len(filtered_data[filtered_data["Provoked/unprovoked"] == "unprovoked"])
    most_common_species = filtered_data["Shark.common.name"].mode().iloc[0] if not filtered_data.empty else "N/A"

    card_style = {
        'padding': '20px',
        'border-radius': '10px',
        'text-align': 'center',
        'color': 'white',
        'width': '23%',
        'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
        'transition': 'transform 0.3s ease',
    }

    summary_cards = [
        html.Div([
            html.H4("Total Incidents", style={'margin': '0', 'font-size': '14px'}),
            html.H2(f"{total_incidents:,}", style={'margin': '10px 0', 'font-size': '24px'}),
        ], className="card", style={**card_style, 'background-color': '#3498DB'}),

        html.Div([
            html.H4("Fatal Incidents", style={'margin': '0', 'font-size': '14px'}),
            html.H2(f"{fatal_incidents:,}", style={'margin': '10px 0', 'font-size': '24px'}),
            html.P(f"({(fatal_incidents / total_incidents * 100):.1f}%)", style={'margin': '0', 'font-size': '12px'}),
        ], className="card", style={**card_style, 'background-color': '#E74C3C'}),

        html.Div([
            html.H4("Unprovoked Incidents", style={'margin': '0', 'font-size': '14px'}),
            html.H2(f"{unprovoked_incidents:,}", style={'margin': '10px 0', 'font-size': '24px'}),
            html.P(f"({(unprovoked_incidents / total_incidents * 100):.1f}%)",
                   style={'margin': '0', 'font-size': '12px'}),
        ], className="card", style={**card_style, 'background-color': '#1ABC9C'}),

        html.Div([
            html.H4("Most Common Species", style={'margin': '0', 'font-size': '14px'}),
            html.H2(most_common_species, style={'margin': '10px 0', 'font-size': '18px', 'word-wrap': 'break-word'}),
        ], className="card", style={**card_style, 'background-color': '#9B59B6'}),
    ]

    return map_fig, trend_fig, activity_fig, summary_cards


if __name__ == "__main__":
    app.run_server(debug=True)