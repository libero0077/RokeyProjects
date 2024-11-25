import requests

def start_server():
    # API endpoint URL
    url = ""  # Adjust host/port and team name
    # Parameters
    params = {
        "model_id": ""  # Replace with actual model ID
    }
    
    # Send POST request
    response = requests.post(url, params=params)
    
    # Check if request was successful
    if response.status_code == 200:
        print("Server started successfully!")
        print("Response:", response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def main():
    start_server()

if __name__ == "__main__":
    main()
