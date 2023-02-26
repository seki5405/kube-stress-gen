from kubernetes import client, config
# from config_loader import config
from job_gen import JobGenerator
import time

# Load the Kubernetes configuration
config.load_kube_config()

# Load scenario
scenario_file = "scenario-2023-02-26.csv"
scenario_path = "scenarios/" + scenario_file
scenario = []
with open(scenario_path, "r") as f:
    lines = f.readlines()
    for line in lines:
        scenario.append(line.strip().split(","))

# Create the Kubernetes API client
batch_api = client.BatchV1Api()

scenario_start_time = time.time()

# While running this program, checking how many minutes have passed since the start of the scenario
idx = 0
while True:
    # Print the current minute from the start of the scenario
    current_minute = int((time.time() - scenario_start_time) / 60)
    print("Current minute: " + str(current_minute))

    current_job = scenario[idx]
    # If the current minute is equal to the minute of the current job, create the job
    if current_minute >= int(current_job[-1]):
        # Create a job
        job_generator = JobGenerator(current_job[1], int(current_job[2]), int(current_job[3]), config)
        job = job_generator.generate_job()
        batch_api.create_namespaced_job(namespace="default", body=job)
        print("Created a job: " + job.metadata.name)
        idx += 1

    time.sleep(5)