import pandas as pd
from utilities.download_utilities import (
    filter_metadata,
    make_experiment_folder,
    get_section_ids,
    download_image,
)


# Filter criteria
FILTER_CRITERIA = {
    "animal_id": "ALL",
    "animal_name": "ALL",
    "experiment_id": "ALL",
    "sex": "ALL",
    "gene": "Calb1",
    "age": ["P4", "P14", "P28"],
    "plane_of_section": "coronal",
    "sleep_state": "Nothing",
    "probe_orientation": ["Nothing", "2"],
}

metadata = pd.read_csv(r"metadata/allen_ISH.csv")
if len(metadata) == 0:
    raise ValueError("Empty metadata file")

# Apply filters
for key, value in FILTER_CRITERIA.items():
    metadata = filter_metadata(metadata, key, value)

for index, row in metadata.iterrows():
    make_experiment_folder("downloaded_data", row["animal_name"], row["experiment_id"])
    section_images = get_section_ids(row["experiment_id"])
    for section_image in section_images:
        download_image(
            "downloaded_data",
            row["animal_name"],
            row["experiment_id"],
            section_image["id"],
            section_image["section_number"],
            view="expression",
        )
        download_image(
            "downloaded_data",
            row["animal_name"],
            row["experiment_id"],
            section_image["id"],
            section_image["section_number"],
            resolution=section_image["resolution"],
        )
