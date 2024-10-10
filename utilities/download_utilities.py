import requests
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
    json_tree = send_query("http://api.brain-map.org/api/v2/data/SectionDataSet/{}.json",brainID,{"include":"equalization,section_images"})