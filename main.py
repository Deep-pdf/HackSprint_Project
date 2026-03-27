import pandas as pd

def find_smart_heatwaves():
    print("Loading historical climate data...")
    filename = "kolkata_dynamic_10yr_temps.csv"
    
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'.")
        return

    # Ensure dates are in the correct format and chronological order
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    # --- YOUR LOGIC COMES TO LIFE HERE ---
    
    # 1. The Context (Past 21 Days Average)
    # This looks at the previous 21 days to know what the CURRENT season feels like
    df['21_Day_Avg'] = df['Max_Temp_C'].rolling(window=21).mean()
    
    # 2. The Wiggle Room (Standard Deviation)
    # This calculates how much the temp naturally fluctuates right now
    df['21_Day_Std'] = df['Max_Temp_C'].rolling(window=21).std()
    
    # 3. The "Sudden Spike" Threshold
    # We say an anomaly is the 21-day average PLUS two times the normal wiggle room
    df['Upper_Danger_Limit'] = df['21_Day_Avg'] + (2 * df['21_Day_Std'])
    
    # 4. Flag the Anomaly!
    # If today is hotter than the danger limit, it's a sudden extreme spike
    df['Is_Anomaly'] = df['Max_Temp_C'] > df['Upper_Danger_Limit']
    
    # Drop the first 20 days because they don't have enough history to make a 21-day average
    df = df.dropna()

    # Filter to only show the extreme days
    anomalies_df = df[df['Is_Anomaly'] == True].copy()
    
    print(f"\nAnalysis Complete! Found {len(anomalies_df)} sudden, unseasonal heat spikes.")
    print("\nHere are the 5 most recent anomalies, showing WHY they were flagged:")
    
    # Show exactly what the AI was thinking
    columns_to_show = ['Date', 'Max_Temp_C', '21_Day_Avg', 'Upper_Danger_Limit']
    print(anomalies_df[columns_to_show].tail())

    # Save it for the Web Map!
    anomalies_df.to_csv("smart_kolkata_anomalies.csv", index=False)
    print("\nSaved anomalies to 'smart_kolkata_anomalies.csv'. Ready for the UI!")

# Run it
find_smart_heatwaves()