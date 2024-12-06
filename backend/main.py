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
        file_path = os.path.join(os.path.dirname(__file__),
                                 "Australian Shark-Incident Database Public Version.xlsx")
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
            # Clean numerical values
            df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
            df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

            # Ensure the shark name column is correctly handled
            if 'shark.common.name' in df.columns:
                df = df.rename(columns={'shark.common.name': 'Shark.common.name'})

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
            data = {
                'incidents': [{
                    'Incident.year': 2020,
                    'State': 'NSW',
                    'Location': 'Byron Bay',
                    'Latitude': -28.6474,
                    'Longitude': 153.6020,
                    'Victim.activity': 'Surfing',
                    'Shark.common.name': 'White shark',
                    'Victim.injury': 'Minor'
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