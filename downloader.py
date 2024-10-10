import pandas as pd
from utilities.download_utilities import filter_metadata
import os 

# Filter criteria
FILTER_CRITERIA = {
    "animal_id": "ALL",
    "animal_name": "ALL",
    "experiment_id": "ALL",
    "sex": "ALL",
    "gene": "Calb1",
    "age": ['P4', 'P14', 'P28'],
    "plane_of_section": "coronal",
    "sleep_state": "Nothing",
    "probe_orientation": ["Nothing", "2"]
}

def make_experiment_folder(target_path, animal_name, experiment_id):
    output_path = os.path.join(target_path, animal_name, str(experiment_id))
    os.makedirs(os.path.join(output_path, '10um'), exist_ok=True)
    os.makedirs(os.path.join(output_path, '25um'), exist_ok=True)
    os.makedirs(os.path.join(output_path, 'expression'), exist_ok=True)

metadata = pd.read_csv(r"metadata/allen_ISH.csv")
if len(metadata) == 0:
    raise ValueError("Empty metadata file")

# Apply filters
for key, value in FILTER_CRITERIA.items():
    metadata = filter_metadata(metadata, key, value)

for index, row in metadata.iterrows():
    make_experiment_folder('downloaded_data', row['animal_name'], row['experiment_id'])
    

