import pandas as pd
import os
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
    "gene": "ALL",
    "age": ["P56"],
    "plane_of_section": "coronal",
    "sleep_state": "Nothing",
    "probe_orientation": ["Nothing", "2"],
}

#This file csv file is created by data scraper py
metadata = pd.read_csv(r"metadata/allen_ISH.csv")
if len(metadata) == 0:
    raise ValueError("Empty metadata file")

# Apply filters
for key, value in FILTER_CRITERIA.items():
    metadata = filter_metadata(metadata, key, value)

#this can be used to see if the files already exist in a specified directory, and if they do skip them.
out_template = r"/mnt/g/AllenDataalignmentProj/resolutionPixelSizeMetadata/ISH/{}/{}"

for index, row in metadata.iterrows():
    if row['treatment'] == "NISSL":
        out_path = out_template.format(row['animal_name'], "NISSL")
        folder = "NISSL"
    else:
        out_path = out_template.format(row['animal_name'], row['experiment_id'])
        folder = row['experiment_id']
    if os.path.isdir(out_path):
        continue
    make_experiment_folder("downloaded_data", row["animal_name"], folder)
    section_images = get_section_ids(row["experiment_id"])
    for section_image in section_images:
        if not row['treatment'] == "NISSL":
            download_image(
                "downloaded_data",
                row["animal_name"],
                folder,
                section_image["id"],
                section_image["section_number"],
                view="expression",
            )
        download_image(
            "downloaded_data",
            row["animal_name"],
            folder,
            section_image["id"],
            section_image["section_number"],
            resolution=section_image["resolution"],
        )
