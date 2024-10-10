import requests
import pandas as pd
from utilities.api_utilities import fetch_data

"""
This requests only 
#This was removed ## coronal data (plane_of_section eq 1)
non transgenic mice only (specimen(donor[transgenic_mouse_id$eqnull]))
Black 6 only (specimen(donor[strain$eq%27C57BL/6J%27]))
ISH data only (treatments[name$eq%27ISH%27])
AntiSense probes only (probes[orientation_id$eq%272%27])
"""


BASE_URL = "https://mouse.brain-map.org/api/v2/data/query.json"
CRITERIA = "criteria=model::SectionDataSet,rma::criteria,specimen(donor[transgenic_mouse_id$eqnull]),specimen(donor[strain$eq%27C57BL/6J%27]),treatments[name$eq%27ISH%27],probes[orientation_id$eq%272%27]&include=plane_of_section,genes,treatments,specimen(donor(age))"
NUM_ROWS = 500


data = fetch_data(BASE_URL, CRITERIA, NUM_ROWS)

data = {
    "animal_id":[],
    "animal_name":[],
    "experiment_id":[],
    "sex":[],
    "gene":[],
    "age":[],
    "plane_of_section":[],
    "treatment":[],
}

for row in api_data:
    animal_id_API = row['specimen_id']
    animal_name = row['specimen']['name']
    experiment_id = row['id']
    sex = row['specimen']['donor']['sex_full_name']
    age = row['specimen']['donor']['age']['days']
    plane_of_section = row["plane_of_section"]["name"]
    if len(row["treatments"]) > 1:
        raise Exception("more than one treatment")
    if len(row['genes']) > 1:
        raise Exception("more than one gene")
    treatment = row["treatments"][0]["name"]
    gene = row['genes'][0]['acronym']
    data["animal_id"].append(animal_id_API)
    data["experiment_id"].append(experiment_id)
    data["sex"].append(sex)
    data["age"].append(age)
    data["plane_of_section"].append(plane_of_section)
    data["animal_name"].append(animal_name)
    data["gene"].append(gene)
    data["treatment"].append(treatment)


# Convert to DataFrame for further processing
df = pd.DataFrame(data)
df.to_csv('metadata/allen_ISH.csv')