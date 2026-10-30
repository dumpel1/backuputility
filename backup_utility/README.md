\# 💾 Multi-Source Local Backup Utility (Web UI)



A robust, production-grade Python script designed to compile multiple arbitrary source directories into a unified, secure ZIP archive. It features a lightweight, responsive \*\*Web Interface\*\* powered by Streamlit, automated rotation (retention) policies, and intelligent filtering of systemic digital clutter.



\---



\## 🚀 Key Features



\- \*\*Multi-Source Bundling:\*\* Add multiple absolute paths dynamically into a single structured backup archive.

\- \*\*Intelligent Clutter Isolation:\*\* Automatically traverses file trees while aggressively ignoring service artifacts (`.git`, `\_\_pycache\_\_`, `venv`, `.idea`, `.vscode`).

\- \*\*Stateful Retention Management:\*\* Built-in engine tracking modification times to delete historical backups older than a user-defined threshold.

\- \*\*Edge-Case Validation:\*\* Native prevention of file-system recursion loops (e.g., stopping a user from backing up an archive into itself) and proactive empty directory checks via `os.scandir`.

\- \*\*Modern Web UI:\*\* Decoupled Model-View architecture rendering an intuitive control panel in the browser.



\---



\## 🛠️ Architecture \& Technologies



\- \*\*Language:\*\* Python 3.10+

\- \*\*Frontend / Interface:\*\* Streamlit (Stateful Session Management via `st.session\_state`)

\- \*\*Core Libraries:\*\* `pathlib` (Object-Oriented Paths), `zipfile` (Archiving Engine), `os` \& `logging`.



The codebase explicitly adheres to \*\*MVC (Model-View-Controller)\*\* principles. Core file manipulation, processing, and traversal routines reside fully separated within `backup\_logic.py`, ensuring maximum scalability and unit-test compatibility.



\---



\## 📦 Installation \& Setup



1\. \*\*Clone the Repository:\*\*

&#x20;  ```bash

&#x20;  git clone https://github.com

&#x20;  cd backup\_utility

&#x20;  ```



2\. \*\*Install Dependencies:\*\*

&#x20;  ```bash

&#x20;  pip install -r requirements.txt

&#x20;  ```



\---



\## 🏃 Execution



\### Method 1: Desktop Shortcut (Windows Only)

Simply double-click the `runweb.bat` script located in the project root. It handles environment setups and launches the application automatically.



\### Method 2: Manual Terminal Launch

Execute the system wrapper directly via your shell:

```bash

python -m streamlit run app\_web.py

```

Once deployed, navigating to `http://localhost:8501` inside your web browser will present the interface.



\---

