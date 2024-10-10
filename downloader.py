import pandas as pd
from utilities.download_utilities import send_query, filter_metadata

ANIMAL_ID = "ALL"
ANIMAL_NAME = "ALL"
EXPERIMENT_ID = "ALL"
SEX = "ALL"
GENE = "ALL"
AGE = "ALL"
PLANE_OF_SECTION = "ALL"

metadata = pd.read_csv(r"metadata/allen_ISH.csv")
if len(metadata) == 0:
    raise ValueError("Empty metadata file")

# Apply filters
metadata = filter_metadata(metadata, "animal_id", ANIMAL_ID)
metadata = filter_metadata(metadata, "animal_name", ANIMAL_NAME)
metadata = filter_metadata(metadata, "experiment_id", EXPERIMENT_ID)
metadata = filter_metadata(metadata, "sex", SEX)
metadata = filter_metadata(metadata, "gene", GENE)
metadata = filter_metadata(metadata, "age", AGE)
metadata = filter_metadata(metadata, "plane_of_section", PLANE_OF_SECTION)

