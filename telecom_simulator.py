# Telecom Traffic Flow Simulator using Queuing Theory

import simpy
import random
import matplotlib.pyplot as plt
import numpy as np

# Parameters
RANDOM_SEED = 42
CALL_ARRIVAL_RATE = 5       # Average number of calls per minute (lambda)
SERVICE_RATE = 6            # Average number of calls handled per minute (mu)
NUM_SERVERS = 2             # Number of servers (e.g., telecom channels)
SIM_TIME = 100              # Simulation time in minutes

# Metrics to collect
wait_times = []
queue_lengths = []
utilization = []

def call(env, name, server):
    arrival_time = env.now
    with server.request() as request:
        yield request
        wait = env.now - arrival_time
        wait_times.append(wait)
        service_time = random.expovariate(SERVICE_RATE)
        yield env.timeout(service_time)

def arrival_process(env, server):
    while True:
        yield env.timeout(random.expovariate(CALL_ARRIVAL_RATE))
        env.process(call(env, f'Call_{int(env.now)}', server))
        queue_lengths.append(len(server.queue))

def monitor_utilization(env, server):
    while True:
        utilization.append(server.count / NUM_SERVERS)
        yield env.timeout(1)

# Run the simulation
random.seed(RANDOM_SEED)
env = simpy.Environment()
server = simpy.Resource(env, capacity=NUM_SERVERS)
env.process(arrival_process(env, server))
env.process(monitor_utilization(env, server))
env.run(until=SIM_TIME)

# Results
print(f"Average wait time: {np.mean(wait_times):.2f} minutes")
print(f"Max queue length: {max(queue_lengths)}")
print(f"Average utilization: {np.mean(utilization) * 100:.2f}%")

# Plots
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.hist(wait_times, bins=20, color='skyblue', edgecolor='black')
plt.title('Wait Times Distribution')
plt.xlabel('Minutes')
plt.ylabel('Number of Calls')

plt.subplot(1, 3, 2)
plt.plot(queue_lengths, color='orange')
plt.title('Queue Length Over Time')
plt.xlabel('Event')
plt.ylabel('Queue Length')

plt.subplot(1, 3, 3)
plt.plot(utilization, color='green')
plt.title('Server Utilization Over Time')
plt.xlabel('Minute')
plt.ylabel('Utilization')

plt.tight_layout()
plt.show()
