import requests
import os
# the send_query function is taken from the ecallen package
def send_query(query_base,spec_id,args):
    response = requests.get(query_base.format(spec_id),params=args)
    if response.ok:
        json_tree = response.json()
        if json_tree['success']:
            return json_tree
        else:
            exception_string = 'did not complete api query successfully'
    else:
        exception_string = 'API failure. Allen says: {}'.format(response.reason)
    # raise an exception if the API request failed
    raise ValueError(exception_string)

def filter_metadata(metadata, column_name, filter_value):
    if filter_value != "ALL":
        if isinstance(filter_value, list):
            metadata = metadata[metadata[column_name].isin(filter_value)]
        else:
            filter_value = str(filter_value)
            metadata = metadata[metadata[column_name] == filter_value]
        if len(metadata) == 0:
            raise ValueError(f"No data found with the specified {column_name.upper()}(S)")
    return metadata

def get_section_ids(experiment_id):
    response = send_query("http://api.brain-map.org/api/v2/data/SectionDataSet/{}.json",experiment_id,{"include":"equalization,section_images"})
    response = response['msg']
    section_images = response[0]['section_images']
    section_images = [i for i in section_images if i is not None]
    return section_images


def make_experiment_folder(output_dir, animal_name, experiment_id):
    output_path = os.path.join(output_dir, animal_name, str(experiment_id))
    os.makedirs(os.path.join(output_path, '10um'), exist_ok=True)
    os.makedirs(os.path.join(output_path, '25um'), exist_ok=True)
    os.makedirs(os.path.join(output_path, 'expression'), exist_ok=True)