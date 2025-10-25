import pandas as pd

# Load the datasets provided by the user
airline = pd.read_csv("datasets/airline.csv")
airport = pd.read_csv("datasets/airport.csv")
seat = pd.read_csv("datasets/seat.csv")
lounge = pd.read_csv("datasets/lounge.csv")

# Show basic structure of each dataset (columns only, for brevity)
myMap = {
    "airline_columns": airline.columns.tolist(),
    "airport_columns": airport.columns.tolist(),
    "seat_columns": seat.columns.tolist(),
    "lounge_columns": lounge.columns.tolist()
}

for key, value in myMap.items():
    print(f"{key}: {value}")