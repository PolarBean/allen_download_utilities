import pandas as pd
from utilities.download_utilities import filter_metadata, make_experiment_folder, get_section_ids
import requests
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



metadata = pd.read_csv(r"metadata/allen_ISH.csv")
if len(metadata) == 0:
    raise ValueError("Empty metadata file")

# Apply filters
for key, value in FILTER_CRITERIA.items():
    metadata = filter_metadata(metadata, key, value)


def download_image(output_dir, animal_name, experiment_id, image_id, image_number, view=None):
    """
    view can be either expression or None
    """
    allen_api  = "http://api.brain-map.org/api/v2/image_download/"
    download_pattern = "{}{}?downsample={}&quality=100"
    if view == 'expression':
        url = download_pattern.format(allen_api, image_id, 0) + '&view=expression&filter=colormap&filterVals=0,1,0,256,0'
        image = requests.get(url, stream=True)
        output_path = os.path.join(output_dir, animal_name, str(experiment_id), "expression", f"{image_id}_s{image_number:04}.jpg")
    with open(output_path, "wb") as f:
        for chunk in image.iter_content(chunk_size=65536):
            if chunk:
                f.write(chunk)
    
for index, row in metadata.iterrows():
    make_experiment_folder('downloaded_data', row['animal_name'], row['experiment_id'])
    section_images = get_section_ids(row['experiment_id'])

    for section_image in section_images:
        download_image('downloaded_data', row['animal_name'], row['experiment_id'], section_image['id'], section_image['section_number'], view='expression')
        break
    break

