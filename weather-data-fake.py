import random
import time
from datetime import datetime
from faker import Faker
from clickhouse_connect import get_client


# Initialize Faker and ClickHouse client
fake = Faker()

# Initialize the client using get_client
clickhouse_client = get_client(host='localhost', port=10200, username='default', password='shard1', database='default')


# Table details
TABLE_NAME = 'station_metrics_distributed'

# Station and data ranges
STATION_IDS = [1, 2, 3, 4]  # 4 stations
TEMPERATURE_RANGE = (0, 45)  # Celsius
HUMIDITY_RANGE = (0, 100)    # Percentage
WIND_SPEED_RANGE = (0, 100)  # km/h
PRESSURE_RANGE = (980, 1000) # hPa

# Function to generate a random data record
def generate_fake_data():
    return {
        "stationId": random.choice(STATION_IDS),
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # ClickHouse DateTime format
        "temperature": round(random.uniform(*TEMPERATURE_RANGE), 2),
        "humidity": round(random.uniform(*HUMIDITY_RANGE), 2),
        "windSpeed": round(random.uniform(*WIND_SPEED_RANGE), 2),
        "pressure": round(random.uniform(*PRESSURE_RANGE), 2)
    }

# Function to insert data into ClickHouse
def insert_data(client, data):
    insert_query = f"""
    INSERT INTO {TABLE_NAME} (stationId, timestamp, temperature, humidity, windSpeed, pressure)
    VALUES (%(stationId)s, %(timestamp)s, %(temperature)s, %(humidity)s, %(windSpeed)s, %(pressure)s)
    """
    client.command(insert_query, parameters=data)
    print(f"Inserted: {data}")

# Generate and insert data in a loop
try:
    for i in range(1, 14180):
        fake_data = generate_fake_data()
        insert_data(clickhouse_client, fake_data)
except KeyboardInterrupt:
    print("Data generation stopped.")
