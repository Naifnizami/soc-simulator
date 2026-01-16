from simulators.azure_simulator import AzureAlertSimulator
from simulators.falcon_simulator import FalconTelemetrySimulator
from engine.soar_engine import SOAREngine
from utils.config import Config
from utils.logger import Logger
import time
import threading


def start_azure_simulator():
    azure = AzureAlertSimulator()
    while True:
        alert = azure.generate_alert()
        azure.write_to_log(alert)
        time.sleep(3)   # Azure alerts every 3 seconds


def start_falcon_simulator():
    falcon = FalconTelemetrySimulator()
    while True:
        event = falcon.generate_event()
        falcon.write_to_log(event)
        time.sleep(2)   # Falcon telemetry every 2 seconds


def start_soar_engine():
    logger = Logger("soar", "soar_engine.log")
    config = Config
    soar = SOAREngine(config, logger)
    soar.run()


if __name__ == "__main__":
    # Run all components in parallel using threads
    t1 = threading.Thread(target=start_azure_simulator)
    t2 = threading.Thread(target=start_falcon_simulator)
    t3 = threading.Thread(target=start_soar_engine)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()