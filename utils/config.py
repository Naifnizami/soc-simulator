class Config:
    """
    Central configuration for the SOAR engine.
    Holds detection rules and policy settings.
    """

    # Ports considered dangerous for inbound connections
    BLOCKED_PORTS = ["3389", "445", "23", "21"]

    # Suspicious command-line arguments for EDR detection
    SUSPICIOUS_ARGS = [
        "-w hidden",
        "Invoke-WebRequest",
        "base64"
    ]