import json
import random
from datetime import datetime
from utils.logger import Logger


class AzureAlertSimulator:
    # FIX: Change default to point inside logs/ folder
    def __init__(self, log_file="logs/defender_logs.json"):
        self.vm_names = ["DB-Prod-01", "Web-FrontEnd-UAE", "AD-Server-Backup"]
        self.log_file = log_file

        # This line was already correct!
        self.logger = Logger("azure", "logs/azure_simulator.log")

    def generate_alert(self):
        is_critical = random.choice([True, False, False, False, False])

        alert = {
            "id": f"azure-{random.randint(10000, 99999)}",
            "vendorInformation": {
                "provider": "Microsoft Defender for Cloud",
                "vendor": "Microsoft"
            },
            "severity": "High" if is_critical else "Low",
            "title": "Suspicious execution of hidden process" if is_critical else "Missing MFA on Admin Account",
            "description": "Detected process running with hidden parameters." if is_critical else "Secure Score impact.",
            "azure_resource_id": f"/subscriptions/sub-123/resourceGroups/prod/providers/Microsoft.Compute/virtualMachines/{random.choice(self.vm_names)}",
            "networkConnections": [
                {
                    "destinationPort": "445" if is_critical else "443",
                    "direction": "Inbound",
                    "sourceAddress": f"192.168.1.{random.randint(5, 255)}"
                }
            ],
            "generated_time": datetime.now().isoformat()
        }

        return alert

    def write_to_log(self, alert):
        with open(self.log_file, "a") as f:
            f.write(json.dumps(alert) + "\n")

        self.logger.info(f"Generated Azure alert: {alert['title']} ({alert['severity']})")