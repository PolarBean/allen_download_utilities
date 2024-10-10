def fetch_data(base_url, criteria, num_rows):
    start_row = 0
    all_data = []

    while True:
        request_str = f"{base_url}?{criteria}&num_rows={num_rows}&start_row={start_row}"
        response = requests.get(request_str)

        if response.status_code == 200:
            data = response.json()["msg"]
            if not data:
                break
            all_data.extend(data)
            start_row += num_rows
        else:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

    return all_data
