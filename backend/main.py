from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os
import numpy as np

app = Flask(__name__)
CORS(app)


def clean_data_for_json(obj):
    if isinstance(obj, (np.int64, np.int32)):
        return int(obj)
    if isinstance(obj, (np.float64, np.float32)):
        return float(obj)
    if isinstance(obj, pd.Series):
        return obj.to_dict()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if pd.isna(obj):
        return None
    return obj


def load_data():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "Australian Shark-Incident Database Public Version.xlsx")
        if os.path.exists(file_path):
            # Columns to keep
            columns_to_keep = [
                'Incident.year', 'Incident.month', 'Victim.injury', 'State', 'Location',
                'Latitude', 'Longitude', 'Site.category', 'Shark.common.name',
                'Victim.activity'
            ]
            # Load data and keep selected columns
            df = pd.read_excel(file_path)
            df = df[columns_to_keep]

            # Drop rows with missing Latitude and Longitude
            df = df.dropna(subset=['Latitude', 'Longitude'])

            # Convert Latitude and Longitude to numeric values
            df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
            df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

            # Drop rows with invalid coordinates
            df = df.dropna(subset=['Latitude', 'Longitude'])

            # Create a datetime column for filtering
            df['Incident.date'] = pd.to_datetime(
                df['Incident.year'].astype(str) + '-' + df['Incident.month'].astype(str),
                errors='coerce'
            )
            df = df.dropna(subset=['Incident.date'])

            # Fill remaining NaN values with 'Unknown'
            df = df.fillna('Unknown')

            return df

        return None
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None


@app.route('/data')
def get_data():
    try:
        df = load_data()

        if df is not None:
            # Convert DataFrame to records and clean data
            incidents = df.fillna('').to_dict('records')
            incidents = [{k: clean_data_for_json(v) for k, v in record.items()}
                         for record in incidents]

            yearly = df['Incident.year'].value_counts().to_dict()
            yearly = {str(k): int(v) for k, v in yearly.items()}

            states = df['State'].value_counts().to_dict()
            states = {str(k): int(v) for k, v in states.items() if pd.notna(k)}

            activities = df['Victim.activity'].value_counts().to_dict()
            activities = {str(k): int(v) for k, v in activities.items() if pd.notna(k)}

            data = {
                'incidents': incidents,
                'yearly': yearly,
                'states': states,
                'activities': activities
            }
        else:
            # Sample data if no real data available
            data = {
                'incidents': [{
                    'Incident.year': 2020,
                    'State': 'NSW',
                    'Location': 'Byron Bay',
                    'Latitude': -28.6474,
                    'Longitude': 153.6020,
                    'Victim.activity': 'Surfing'
                }],
                'yearly': {
                    '2018': 15,
                    '2019': 20,
                    '2020': 18,
                    '2021': 25,
                    '2022': 22
                },
                'states': {
                    'NSW': 40,
                    'QLD': 30,
                    'WA': 20,
                    'VIC': 10
                },
                'activities': {
                    'Swimming': 30,
                    'Surfing': 45,
                    'Diving': 15,
                    'Fishing': 10
                }
            }

        return jsonify(data)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("Server starting on http://localhost:5349")
    app.run(host='0.0.0.0', port=5349, debug=True)
