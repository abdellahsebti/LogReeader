# 🛡️ LogReeader

> **AI-Powered Security Log Analyzer** — Detect anomalies, get AI insights, and monitor your system — all locally, all private.

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![ML](https://img.shields.io/badge/ML-Scikit--learn-orange.svg)
![AI](https://img.shields.io/badge/AI-Ollama-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🖼️ Screenshot](#️-screenshot)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [🤖 Ollama AI Setup](#-ollama-ai-setup)
- [📁 Project Structure](#-project-structure)
- [⚙️ Configuration](#️-configuration)
- [🔍 How It Works](#-how-it-works)
- [🧪 Testing](#-testing)
- [❓ Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

### 🔐 Security Monitoring
- ✅ **Real-time log ingestion** from Windows Event Logs or Linux `/var/log`
- ✅ **Automatic anomaly detection** using Isolation Forest ML algorithm
- ✅ **Suspicious activity highlighting** with color-coded risk levels

### 🤖 AI-Powered Insights (Optional)
- ✅ **Local LLM analysis** via Ollama (Llama 3, Phi-3, Mistral)
- ✅ **Natural language explanations** of security events
- ✅ **Actionable remediation recommendations**
- ✅ **Executive security summaries** in plain English

### 🎨 Beautiful Dashboard
- ✅ **Modern dark theme** with gradient accents
- ✅ **Responsive design** — works on desktop, tablet, mobile
- ✅ **Animated statistics** and interactive tables
- ✅ **Toast notifications** for user feedback

### 🔒 Privacy-First
- ✅ **100% local processing** — no data leaves your machine
- ✅ **No cloud dependencies** — works offline
- ✅ **SQLite database** — simple, portable storage

---

## 🖼️ Screenshot

```
┌─────────────────────────────────────────────────────┐
│ 🛡️ LogSentinel                                      │
│ AI-Powered Log Anomaly Detection...                 │
│                                                     │
│ [🪟 Windows] [🖥️ DESKTOP-PC] [📁 Real Logs]        │
│                                                     │
│ [🔍 Run Anomaly Detection]  [🔄 Refresh Logs]      │
│                                                     │
│ ┌─────────────┬─────────────┬─────────────┐        │
│ │ 📊 Total    │ ⚠️ Suspicious│ 🔒 Security │        │
│ │    45       │     4       │    91%      │        │
│ └─────────────┴─────────────┴─────────────┘        │
│                                                     │
│ 🤖 AI Security Insights [🟢 llama3.2 Ready]        │
│ [🔍 Analyze Suspicious] [📊 Generate Summary]      │
│                                                     │
│ ┌─────────────────────────────────────────┐        │
│ │ ⚠️ HIGH RISK                             │        │
│ │ [2024-01-15] Security(4625): Failed...  │        │
│ │ 💡 Multiple failed logins suggest...    │        │
│ │ 🔧 • Block IP • Enable MFA • Review...  │        │
│ └─────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Backend** | Python 3.11+, Flask 3.0 |
| **Machine Learning** | Scikit-learn (Isolation Forest, TF-IDF) |
| **AI/LLM** | Ollama (local LLMs: Llama 3, Phi-3, Mistral) |
| **Database** | SQLite (embedded, no setup required) |
| **Frontend** | HTML5, CSS3 (inline), Vanilla JavaScript |
| **Log Parsing** | PowerShell (Windows), regex (Linux) |
| **HTTP Client** | `requests` for Ollama API |

---

## 🚀 Quick Start

### Prerequisites

- ✅ **Python 3.11 or 3.12** (3.13+ not yet supported for scikit-learn)
- ✅ **Windows 10/11** or **Linux** (Ubuntu/Debian recommended)
- ✅ **Administrator/root access** (to read system logs)

### Step 1: Clone or Create Project

```bash
# Create project folder
mkdir logsentinel
cd logsentinel

# Create subdirectories
mkdir data templates static
```

### Step 2: Create Files

Copy the following files into your project:

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application + routes |
| `log_reader.py` | Cross-platform log parsing module |
| `ollama_analyzer.py` | Ollama LLM integration (optional) |
| `requirements.txt` | Python dependencies |
| `templates/dashboard.html` | Beautiful web dashboard |

### Step 3: Install Dependencies

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Upgrade pip and install packages
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
# Start the server
python app.py
```

### Step 5: Open in Browser

```
http://localhost:5000
```

✅ You should see your dashboard with real system logs!

---

## 🤖 Ollama AI Setup (Optional but Recommended)

### Step 1: Install Ollama

**Windows:**
1. Download from: https://ollama.com/download
2. Run `Ollama Setup.exe`
3. Accept default installation options

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Step 2: Pull a Model

```bash
# Lightweight & fast (recommended for beginners)
ollama pull phi3

# More powerful (needs 8GB+ RAM)
ollama pull llama3.2

# Balanced option
ollama pull mistral
```

### Step 3: Start Ollama Server

```bash
# Run in background (Windows)
start ollama serve

# Or run in terminal (Linux/Mac)
ollama serve &
```

✅ Keep Ollama running while using LogSentinel.

### Step 4: Configure Model in Code

Edit `app.py` and update the model name:

```python
# Initialize Ollama Analyzer
ollama = OllamaAnalyzer(model="phi3")  # Change to your pulled model
```

### Step 5: Test AI Features

1. Open dashboard at `http://localhost:5000`
2. Click **"🔄 Check Connection"** in AI panel
3. Click **"🔍 Analyze Suspicious Logs"** to see AI insights

---

## 📁 Project Structure

```
logsentinel/
│
├── app.py                 # Main Flask app + API routes
├── log_reader.py          # Cross-platform log parsing
├── ollama_analyzer.py     # Ollama LLM integration
├── requirements.txt       # Python dependencies
│
├── data/
│   └── logs.db           # SQLite database (auto-created)
│
├── templates/
│   └── dashboard.html    # Web dashboard (inline CSS/JS)
│
├── static/
│   └── style.css         # (Optional) External styles
│
├── .venv/                 # Virtual environment (gitignore)
├── .gitignore             # Files to exclude from version control
└── README.md              # This file
```

---

## ⚙️ Configuration

### Environment Variables (Optional)

Create a `.env` file for custom settings:

```env
# Flask settings
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5000

# Log paths
LINUX_LOG_PATH=/var/log/auth.log
WINDOWS_LOG_NAME=Security

# Ollama settings
OLLAMA_MODEL=phi3
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=120

# ML settings
ML_CONTAMINATION=0.1
ML_MAX_FEATURES=100
```

### Customizing the Dashboard

Edit `templates/dashboard.html` to:

- 🎨 Change colors: Modify CSS gradient values
- 📊 Add new stats: Duplicate a `.stat-card` div
- 🔧 Add buttons: Add new `<button>` elements with `onclick` handlers

### Changing the ML Sensitivity

In `app.py`, adjust the `IsolationForest` parameters:

```python
# More sensitive (detects more anomalies)
clf = IsolationForest(contamination=0.2, random_state=42)

# Less sensitive (fewer false positives)
clf = IsolationForest(contamination=0.05, random_state=42)
```

---

## 🔍 How It Works

### 1. Log Collection
```
Windows: PowerShell → Get-WinEvent → JSON parsing
Linux:   Read /var/log/auth.log → Regex parsing
Fallback: Sample data for testing
```

### 2. Data Storage
```
Raw logs → SQLite database → Indexed by timestamp/service
```

### 3. Anomaly Detection (ML)
```
Log messages → TF-IDF vectorization → Isolation Forest → Suspicion score (0 or 1)
```

### 4. AI Analysis (Optional)
```
Suspicious logs → Ollama API → LLM prompt → JSON response → Human-readable insights
```

### 5. Dashboard Display
```
Database query → JSON API → JavaScript render → Interactive HTML table
```

---

## 🧪 Testing

### Test with Sample Data

If system logs aren't accessible, the app auto-falls back to sample data. Verify with:

```bash
python app.py
# Check browser shows "🧪 Sample Data" badge
```

### Test ML Detection

1. Load logs
2. Click **"🔍 Run Anomaly Detection"**
3. Verify suspicious logs are highlighted in red

### Test Ollama Integration

```bash
# Verify Ollama is running
curl http://localhost:11434/api/tags

# Should return: {"models":[...]}
```

### Manual Log Injection (Advanced)

Add test logs directly to SQLite:

```bash
# Open database
.venv\Scripts\activate
python

# In Python shell:
import sqlite3
conn = sqlite3.connect('data/logs.db')
cursor = conn.cursor()
cursor.execute('''
    INSERT INTO logs (timestamp, hostname, service, message, suspicion_score, source)
    VALUES (?, ?, ?, ?, ?, ?)
''', ('2024-01-20 15:30:00', 'TEST-PC', 'Security(ID:4625)', 
      'Failed logon for admin from 192.168.1.999', 1, 'windows'))
conn.commit()
conn.close()
```

---

## ❓ Troubleshooting

### 🔴 Common Issues

| Problem | Solution |
|---------|----------|
| `scikit-learn` install fails | Use Python 3.11 or Conda (see Quick Start) |
| `sqlite3.OperationalError: no column named source` | Delete `data/logs.db` and restart app |
| Ollama "Connection refused" | Run `ollama serve` first |
| No logs showing on Windows | Run PowerShell as Administrator once to enable log access |
| Dashboard shows "Sample Data" | Check if you have permission to read system logs |
| AI analysis too slow | Use `phi3` model instead of `llama3.2` |
| Port 5000 already in use | Change `app.run(port=5000)` to `port=5001` |

### 🔍 Debug Mode

Enable detailed logging:

```python
# In app.py, add before app.run()
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 🪟 Windows-Specific Fixes

**Enable Security Log Access:**
```powershell
# Run PowerShell as Administrator
wevtutil sl Security /ca:O:BAG:SYD:(A;OICI;FA;;;SY)(A;OICI;FA;;;BA)(A;OICI;0x7;;;S-1-5-20)
```

**Check Event Logs Manually:**
```powershell
# Verify logs exist
Get-WinEvent -LogName Security -MaxEvents 5
```

### 🐧 Linux-Specific Fixes

**Grant Log Permissions:**
```bash
# Option 1: Run with sudo
sudo python app.py

# Option 2: Add user to adm group
sudo usermod -aG adm $USER
# (Then logout and login again)
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to help:

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### 💡 Ideas for Contributions

- [ ] Add support for macOS Unified Logging
- [ ] Implement user authentication system
- [ ] Add Chart.js visualizations for log trends
- [ ] Create export to PDF/CSV functionality
- [ ] Add Discord/Slack webhook alerts
- [ ] Support more log formats (Apache, Nginx, Docker)

### 📝 Code Style

- Follow [PEP 8](https://pep8.org) for Python
- Use descriptive variable names
- Add docstrings to new functions
- Test locally before submitting PR

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

```
MIT License

Copyright (c) 2024 LogSentinel Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.com) — For making local LLMs accessible
- [Scikit-learn](https://scikit-learn.org) — For powerful, simple ML tools
- [Flask](https://flask.palletsprojects.com) — For lightweight web development
- [Windows Event Log API](https://learn.microsoft.com/en-us/windows/win32/wes/windows-event-log) — For system logging
- You! — For building security tools that protect systems 🛡️

---

## 📬 Support & Questions

- 🐛 **Bug Reports**: Open an issue on GitHub
- 💬 **Discussions**: Use GitHub Discussions tab
- 📧 **Contact**: [Your Email/Handle Here]

---

> ⚠️ **Disclaimer**: LogSentinel is a security *monitoring* tool, not a replacement for enterprise SIEM solutions. Use it to augment your security posture, not as your sole defense. Always follow security best practices and consult professionals for critical infrastructure.

---

<div align="center">

**🛡️ Built with ❤️ for safer systems**

[⬆️ Back to Top](#-logsentinel)

</div>