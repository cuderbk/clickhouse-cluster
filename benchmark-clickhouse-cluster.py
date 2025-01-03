from clickhouse_connect import get_client
import random
import time
from datetime import datetime

# Initialize the ClickHouse client
clickhouse_client = get_client(host='localhost', port=10200, username='default', password='shard1', database='default')

# Benchmark function
def benchmark_query(query, iterations=100):
    start_time = time.time()
    for _ in range(iterations):
        clickhouse_client.execute(query)
    elapsed_time = time.time() - start_time
    print(f"Executed {iterations} iterations in {elapsed_time:.2f} seconds")
    print(f"Average time per query: {elapsed_time / iterations:.4f} seconds")

# Test Queries
read_query = "SELECT COUNT(*) FROM station_metrics_distributed"
write_query = """
INSERT INTO station_metrics_distributed (stationId, timestamp, temperature, humidity, windSpeed, pressure) 
VALUES (1, now(), 25.5, 65, 10.5, 990)
"""

# Run Benchmarks
print("Read Benchmark:")
benchmark_query(read_query)

print("\nWrite Benchmark:")
benchmark_query(write_query)
