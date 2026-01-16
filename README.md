# 🛡️ SOC Simulator (SIEM/EDR/SOAR)

### A Universal Threat Emulation & Automated Response Engine

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![Architecture](https://img.shields.io/badge/Architecture-Producer--Consumer-orange)
![License](https://img.shields.io/badge/License-MIT-green)

A modular, multi-threaded framework designed to emulate enterprise detection engineering workflows without requiring enterprise licenses. This project simulates the complete lifecycle of a SOC incident: from **CrowdStrike/Sysmon EDR telemetry** generation to **Microsoft Defender for Cloud** alerting, followed by automated **SOAR logic** for containment.

---

## 🏗️ Architecture

The system operates on a **Producer-Consumer model**, simulating a real-time event stream.

```mermaid
graph TD
    subgraph "Threat Generators"
        A[Azure Defender Sim] -->|JSON Stream| Q1[(defender_logs.json)]
        B[Falcon EDR Sim] -->|JSON Stream| Q2[(falcon_logs.json)]
    end

    subgraph "SOAR Engine"
        Q1 --> C{Main_SOAR.py}
        Q2 --> C
        C -->|Parse & Normalize| D[Detection Logic Gates]
        
        D -->|Cond: Port 445 + High Sev| E[Azure Response Module]
        D -->|Cond: Hidden PowerShell| F[Falcon Response Module]
    end

    subgraph "Automated Actions"
        E -->|API Call Stub| G[BLOCK Network Traffic]
        F -->|API Call Stub| H[ISOLATE Host]
    end

    style C fill:#f96,stroke:#333,stroke-width:2px
    style G fill:#f9f,stroke:#333,stroke-width:2px
    style H fill:#f9f,stroke:#333,stroke-width:2px
```

---

## 🚀 Setup & Usage

### 1. Installation
Clone the repository:
```bash
git clone https://github.com/Naifnizami/soc-simulator.git
cd soc-simulator
```

### 2. Run with Docker (Recommended)
This launches the complete microservices architecture (Generators + SOAR Engine + Log Volume).
```bash
docker-compose up --build
```

### 3. Observe Automation
You will see real-time colored log ingestion and logic triggers in the terminal:

```text
[Falcon] Agent Sent Telemetry: \Device\...\powershell.exe
[!!!] SOAR TRIGGERED: EDR Malware Detected on DESKTOP-HR-DUBAI-05
      ---> ACTION: API Call 'falconpy.hosts.update_device_tags(Action=ISOLATE)'
```

---

## 🛠️ Components

| Component | Function | Simulation Target |
| :--- | :--- | :--- |
| **azure_simulator.py** | Generates CSPM/CWP alerts | `Microsoft.Security/alerts` API |
| **falcon_simulator.py** | Generates Process Events | `ProcessRollup2` EDR Events |
| **soar_engine.py** | Ingests JSON, applies Rules | Splunk/FortiSOAR Playbooks |

---

## 🗺️ Roadmap
- [ ] **External Ingestion:** Add Splunk HEC support to push simulated logs to a real SIEM instance.
- [ ] **MITRE Mapping:** Tag simulated alerts with specific MITRE T-Codes (e.g., T1059.001 PowerShell).

---

*This tool is intended for educational purposes and detection engineering research.*
