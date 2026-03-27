import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_and_save_historical_data():
    # 1. Calculate dynamic dates (10 years ago up to 5 days ago)
    today = datetime.now()
    end_date_obj = today - timedelta(days=5)
    start_date_obj = end_date_obj - timedelta(days=3650) 
    
    end_date_str = end_date_obj.strftime('%Y-%m-%d')
    start_date_str = start_date_obj.strftime('%Y-%m-%d')
    
    print(f"Fetching data from {start_date_str} to {end_date_str}...")
    
    # 2. Setup the API request
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": 22.5726,
        "longitude": 88.3639,
        "start_date": start_date_str, 
        "end_date": end_date_str,     
        "daily": "temperature_2m_max",
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    
    # 3. Process and Save the Data
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame({
            'Date': data['daily']['time'],
            'Max_Temp_C': data['daily']['temperature_2m_max']
        })
        
        # --- THE CRUCIAL SAVING STEP ---
        filename = "kolkata_dynamic_10yr_temps.csv"
        df.to_csv(filename, index=False)
        print(f"\nSuccess! 10 years of data permanently saved to '{filename}'")
        # -------------------------------
        
        return df
    else:
        print(f"Failed. Error: {response.status_code}")

# Run the function
df = fetch_and_save_historical_data()