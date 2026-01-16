from simulators.azure_simulator import AzureAlertSimulator
from simulators.falcon_simulator import FalconTelemetrySimulator
from engine.soar_engine import SOAREngine
from utils.config import Config
from utils.logger import Logger
import time
import threading
import os

# Ensure logs folder exists before anything starts
if not os.path.exists("logs"):
    os.makedirs("logs")

def start_azure_simulator():
    # Pass explicit paths to ensure it goes into logs folder
    azure = AzureAlertSimulator(log_file="logs/defender_logs.json")
    # Note: You need to make sure AzureAlertSimulator class also fixes its own internal "azure_simulator.log"
    # But for the JSON data, this fixes it here.
    
    while True:
        alert = azure.generate_alert()
        azure.write_to_log(alert)
        time.sleep(3)


def start_falcon_simulator():
    # Pass explicit paths
    falcon = FalconTelemetrySimulator(log_file="logs/falcon_logs.json")
    
    while True:
        event = falcon.generate_event()
        falcon.write_to_log(event)
        time.sleep(2)


def start_soar_engine():
    # FIX: Point the SOAR internal log to the folder
    logger = Logger("soar", "logs/soar_engine.log")
    
    config = Config
    # FIX: Ensure the engine looks for JSONs in the folder
    soar = SOAREngine(
        config, 
        logger, 
        azure_log="logs/defender_logs.json", 
        falcon_log="logs/falcon_logs.json"
    )
    soar.run()


if __name__ == "__main__":
    print("[*] ORCHESTRATOR STARTING: Spawning Threads...")
    
    t1 = threading.Thread(target=start_azure_simulator)
    t2 = threading.Thread(target=start_falcon_simulator)
    t3 = threading.Thread(target=start_soar_engine)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()