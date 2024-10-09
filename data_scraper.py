import requests
import pandas as pd
from tqdm import tqdm


REQUEST_STR = "https://mouse.brain-map.org/api/v2/data/query.json?criteria=model::SectionDataSet,rma::criteria,[plane_of_section_id$eq1],specimen(donor[strain$eq%27C57BL/6J%27]),treatments[name$eq'ISH'],probes[orientation_id$eq%272%27]&include=plane_of_section,genes,treatments,specimen(donor(age))&num_rows=all"

api_data = requests.get(REQUEST_STR)

api_data.status_code
api_data = api_data.json()["msg"]
data = {
    "animal_id_API":[],
    "animal_name":[],
    "experiment_id":[],
    "sex":[],
    "gene":[],
    "age":[],
    "plane_of_section":[],
    "treatment":[],
    "gene":[]
}

for row in tqdm(api_data):
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
    data["animal_id_API"].append(animal_id_API)
    data["experiment_id"].append(experiment_id)
    data["sex"].append(sex)
    data["age"].append(age)
    data["plane_of_section"].append(plane_of_section)
    data["animal_name"].append(animal_name)
    data["gene"].append(gene)
    data["treatment"].append(treatment)


for k in data.keys():
    print(k, len(data[k]))
# Convert to DataFrame for further processing
df = pd.DataFrame(data)
display(df.head())