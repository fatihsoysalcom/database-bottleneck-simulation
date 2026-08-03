import time
import random

# Simulate a database that can only handle a certain number of queries per second
class SimulatedDatabase:
    def __init__(self, max_queries_per_sec=50):
        self.max_queries_per_sec = max_queries_per_sec
        self.query_count = 0
        self.last_reset_time = time.time()

    def execute_query(self, query_id):
        current_time = time.time()
        # Reset query count if a second has passed
        if current_time - self.last_reset_time >= 1.0:
            self.query_count = 0
            self.last_reset_time = current_time

        # Simulate query processing time
        processing_time = random.uniform(0.01, 0.05) # Simulate some DB work

        # Check if we've hit the query limit for this second
        if self.query_count >= self.max_queries_per_sec:
            # This is the bottleneck: we have to wait
            wait_time = 1.0 - (current_time - self.last_reset_time)
            if wait_time > 0:
                # print(f"[DB] Throttling: Waiting {wait_time:.2f}s for query {query_id}")
                time.sleep(wait_time)
            # Reset after waiting
            self.query_count = 0
            self.last_reset_time = time.time()

        self.query_count += 1
        # print(f"[DB] Executing query {query_id} (count: {self.query_count})")
        time.sleep(processing_time) # Simulate actual query execution
        return f"Result for query {query_id}"

# Simulate an application making requests to the database
def application_worker(db, worker_id, num_queries):
    start_time = time.time()
    for i in range(num_queries):
        query_id = f"{worker_id}-{i}"
        db.execute_query(query_id)
    end_time = time.time()
    print(f"Worker {worker_id} finished {num_queries} queries in {end_time - start_time:.2f}s")

if __name__ == "__main__":
    # Simulate a database with a low query limit (e.g., 10 queries per second)
    # This will cause a bottleneck if the application tries to send more
    db = SimulatedDatabase(max_queries_per_sec=10)

    print(f"Starting simulation with DB limit: {db.max_queries_per_sec} queries/sec")

    # Simulate an application trying to make many requests
    # If we have 5 workers, each doing 20 queries, that's 100 queries total.
    # If the DB can only handle 10/sec, it will take ~10 seconds.
    num_workers = 5
    queries_per_worker = 20
    total_expected_queries = num_workers * queries_per_worker

    print(f"Application attempting to run {total_expected_queries} queries with {num_workers} workers.")

    start_sim_time = time.time()
    threads = []
    for i in range(num_workers):
        # In a real app, these would be threads or async tasks
        application_worker(db, i, queries_per_worker)

    end_sim_time = time.time()
    print(f"\nSimulation finished.")
    print(f"Total queries attempted: {total_expected_queries}")
    print(f"Total simulation time: {end_sim_time - start_sim_time:.2f}s")
    print(f"Average queries per second achieved: {total_expected_queries / (end_sim_time - start_sim_time):.2f}")
    print("\nObserve how the achieved QPS is much lower than the DB's max_queries_per_sec, indicating a bottleneck.")
