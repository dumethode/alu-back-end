import requests

def gather_data_from_api():
    url = "https://api.example.com/data"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

if __name__ == "__main__":
    data = gather_data_from_api()
    if data:
        print(data)
    else:
        print("Failed to retrieve data")