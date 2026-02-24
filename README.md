# 🗺️ GMapScan: Advanced Google Maps API Security Auditor

**GMapScan** is a high-performance, multi-threaded security tool designed to audit Google Maps API keys for common misconfigurations, unauthorized access, and billing status. 



## ✨ Features
* **Parallel Execution:** Uses Python's `ThreadPoolExecutor` for ultra-fast scanning.
* **Billing Detection:** Identifies if a key is "Active/Billed" or "Unbilled" to assess financial risk.
* **2026 Pricing Integration:** Provides estimated costs for 13+ Google Cloud services.
* **Forensic Reporting:** Generates a professional HTML report with Proof-of-Concept (PoC) links.
* **OSINT Metadata:** Attempts to extract Google Cloud Project IDs and Names.

---

## Installation & Usage

### 🛠️ Prerequisites
* Python 3.8+
* `pipx` (Recommended for Linux users to avoid PEP 668 environment errors)

### 📥 Installation
```bash
# Clone the repository
git clone https://github.com/parag25mcf10022/gmapsscan
cd gmapsscan

# Install globally using pipx (Parrot/Kali/Ubuntu)
pipx install .

# OR install via pip
pip install .

**RUN the Tool**
gmapsscan
