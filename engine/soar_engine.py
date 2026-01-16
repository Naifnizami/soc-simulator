import json
import os
import time

class SOAREngine:
    def __init__(self, config, logger, azure_log="defender_logs.json", falcon_log="falcon_logs.json"):
        """
        Constructor: stores config, logger, and log file paths.
        """
        self.config = config
        self.logger = logger
        self.azure_log = azure_log
        self.falcon_log = falcon_log


    def _read_log_file(self, path):
        """
        Internal helper method.
        Reads a log file and returns a list of JSON objects.
        """
        if not os.path.exists(path):
            return []

        events = []
        with open(path, "r") as f:
            for line in f:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    self.logger.error(f"Failed to parse JSON line: {line}")
        return events


    def _clear_log_file(self, path):
        """
        Internal helper method.
        Clears the log file after processing (simulating queue consumption).
        """
        open(path, "w").close()


    def process_azure_alert(self, alert):
        """
        Applies detection logic for Azure Defender alerts.
        """
        try:
            port = alert["networkConnections"][0]["destinationPort"]
            severity = alert["severity"]

            if port in self.config.BLOCKED_PORTS and severity == "High":
                self.logger.warning(
                    f"SOAR ACTION: Blocking port {port} on {alert['azure_resource_id']}"
                )
                return True

        except Exception as e:
            self.logger.error(f"Error processing Azure alert: {e}")

        return False


    def process_falcon_event(self, event):
        """
        Applies detection logic for Falcon EDR telemetry.
        """
        try:
            cmd = event.get("CommandLine", "")

            for signature in self.config.SUSPICIOUS_ARGS:
                if signature in cmd:
                    self.logger.warning(
                        f"SOAR ACTION: Isolating host {event['ComputerName']} due to signature '{signature}'"
                    )
                    return True

        except Exception as e:
            self.logger.error(f"Error processing Falcon event: {e}")

        return False


    def run(self):
        """
        Main SOAR loop.
        Continuously reads logs, processes them, and triggers actions.
        """
        self.logger.info("SOAR Engine started...")

        while True:
            # 1. Read Azure alerts
            azure_events = self._read_log_file(self.azure_log)
            for alert in azure_events:
                self.process_azure_alert(alert)

            # 2. Read Falcon telemetry
            falcon_events = self._read_log_file(self.falcon_log)
            for event in falcon_events:
                self.process_falcon_event(event)

            # 3. Clear logs (simulate queue consumption)
            self._clear_log_file(self.azure_log)
            self._clear_log_file(self.falcon_log)

            time.sleep(1)