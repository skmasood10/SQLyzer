# 🔍 SQLyzzer Center

> *"While most tools look for 'Error' messages, SQLyzzer looks for 'Behavioral Outliers.'"*

A behavioral SQL Injection detection tool that identifies vulnerabilities via **statistical anomalies** in Response Size & Time — capable of catching **Silent** and **Blind** attacks that traditional scanners miss.

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-Modern_UI-1F6AA5?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-Mock_Server-000000?style=for-the-badge&logo=flask&logoColor=white)

---

## 🧠 The Core Idea

Traditional SQLi scanners rely on matching error strings like `syntax error` or `mysql_fetch`. **SQLyzzer takes a different approach** — it treats the server as a black box and watches *how* it behaves, not *what* it says.

Using **Z-Score heuristics**, SQLyzzer flags responses that are mathematically unusual in:
- 📦 **Response Size** → Data Leak detection (Classical SQLi)
- ⏱️ **Response Latency** → Time-Blind attack detection (e.g., `SLEEP()`, `WAITFOR DELAY`)

This makes it effective even when the server returns a clean `200 OK` with no visible error.

---

## ✨ Features

- 📊 **Z-Score Mining** — Applies standard deviation analysis to mathematically isolate anomalous server responses from baseline traffic
- 🎯 **Dual-Vector Detection** — Simultaneously tracks both Data Leak (Size) and Time-Blind (Latency) attack surfaces in real time
- 🧪 **Built-in Mock Environment** — Bundled Flask server for safe, classroom-friendly demonstrations with zero external dependencies
- 📈 **Live Visualization** — Real-time Scatter and Line plots update as payloads are sent
- 📁 **CSV Audit Logs** — Every scan session is exported as a structured CSV for review and reporting

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend / Core Logic** | Python 3.13 |
| **Statistical Analysis** | Pandas, NumPy (Z-Score Processing) |
| **GUI** | CustomTkinter (Modern Dark UI) |
| **Networking** | Requests (HTTP Automation) |
| **Visualization** | Matplotlib (Real-time Analytics) |
| **Mock Target Server** | Flask |

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/skmasood10/SQLyzzer-Center.git
cd SQLyzzer-Center
```

### 2. Install Dependencies
```bash
pip install customtkinter pandas numpy matplotlib requests flask
```

### 3. Launch the Mock Target Server
```bash
python mock_server.py
```
> The vulnerable mock server will start at `http://127.0.0.1:5000`

### 4. Launch the Main Application
```bash
python main_gui.py
```

### 5. Run Your First Scan
Enter the following in the GUI and hit **Start Scan**:
- **Target URL:** `http://127.0.0.1:5000/vulnerabilities/sqli/`
- **Session Cookie:** `PHPSESSID=<your_session_value>`
Baseline Traffic  →  Compute Mean & Std Dev
↓
Inject SQLi Payloads  →  Collect Response Size & Latency
↓
Calculate Z-Score:   Z = (X - μ) / σ
↓
|Z| > Threshold?  →  🚨 ANOMALY FLAGGED (Potential SQLi)
| Z-Score Range | Interpretation |
|---|---|
| `\|Z\| < 2.0` | Normal response — baseline behavior |
| `2.0 ≤ \|Z\| < 3.0` | Suspicious — warrants review |
| `\|Z\| ≥ 3.0` | High confidence anomaly — likely injection |

---

## 🎯 Input & Output

**Input Parameters:**
- Target URL (e.g., `http://127.0.0.1:5000/vulnerabilities/sqli/`)
- Session Cookie (`PHPSESSID` value for authenticated scans)

**Output:**
- Live Scatter plot — Response Size per payload
- Live Line plot — Latency per payload
- `audit_log.csv` — Full structured log of every request, response size, latency, and Z-Score

---

## 🔒 Responsible Use

> ⚠️ **This tool is intended strictly for educational and authorized penetration testing purposes.**

- Always obtain explicit written permission before scanning any target
- Use the built-in **mock server** for all demonstrations and learning
- The authors are not responsible for any misuse of this software
- Never run against production systems without a signed scope agreement

---

## 🔑 System Requirements

- **API Keys:** None — fully self-contained
- **Environment Variables:** None required
- **Network:** Localhost-ready out of the box; internet not required for mock testing
- **OS:** Windows / Linux / macOS (Python 3.13+)

---

## 📦 Requirements Summary

```txt
customtkinter
pandas
numpy
matplotlib
requests
flask
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern dark-themed GUI framework
- [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/) for statistical processing
- [DVWA](https://github.com/digininja/DVWA) for inspiring the mock vulnerable environment concept
- The cybersecurity research community for advancing behavioral anomaly detection

---

<p align="center">Built for defenders, researchers, and students 🛡️ — catching what scanners miss.</p>

