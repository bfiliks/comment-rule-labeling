
![Banner](./assets/streamlit_banner.png)

[![Streamlit App](https://img.shields.io/badge/Live%20Demo-Streamlit-ff4b4b?logo=streamlit&logoColor=white)](https://comment-rule-labeling.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)
[![Issues](https://img.shields.io/github/issues/bfiliks/comment-rule-labeling)](https://github.com/bfiliks/comment-rule-labeling/issues)

> A collaborative tool for labeling **YouTube comments** based on community rules.  
> Built with **Streamlit** and **Google Sheets** to enable multiple annotators to label remotely **without duplication**.

---

## 🚀 Live App

🌐 **Try it out now** → [comment-rule-labeling.streamlit.app](https://comment-rule-labeling.streamlit.app/)

---

## 🖼️ Features

- 🔐 Annotator login with name tracking
- 🗂️ Google Sheets-based collaborative annotation
- 🏷️ Binary labeling:  
  `0` = Not Violating | `1` = Violates Rule
- 🚩 Optional flag for uncertain cases
- 💬 Leave helpful notes/comments
- 📊 Progress tracker: global and per-annotator
- 🔎 Search by keyword for fast filtering
- ➕ / ➖ Navigation across comment-rule pairs
- 🔒 Multi-annotator sync: avoids overwriting or duplicate work

---

## 📁 Folder Structure

```bash
.
├── app.py                    # Main Streamlit app
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml           # App theme and favicon
├── assets/
│   └── streamlit_banner.png  # Header banner
└── README.md                 # You're here!
```

---

## 🧪 Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/bfiliks/comment-rule-labeling.git
cd comment-rule-labeling

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Streamlit app
streamlit run app.py
```

> 🔐 To use Google Sheets Sync:
> - Upload your `gspread_credentials.json` to **Streamlit Secrets**
> - Follow setup at [Streamlit Docs – Secrets](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)

---

## ☁️ Deploy on Streamlit Cloud

1. Push this repo to GitHub  
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)  
3. Click **"New App"**  
4. Select your GitHub repo and `app.py`  
5. Add your `gspread_credentials.json` as [Secrets](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)

---

## 🛠️ How to Use This Tool

1. **Launch the App**
   - Visit: [https://comment-rule-labeling.streamlit.app](https://comment-rule-labeling.streamlit.app)
   - Enter your **annotator name** to begin

2. **Upload the CSV File**
   - Required format: `rule_text`, `text`
   - Ensure your dataset pairs rules with YouTube comments

3. **Label and Annotate**
   - Choose:
     - `0` → Not Violating
     - `1` → Violates Rule
   - Optionally:
     - 🚩 Flag the sample
     - Add a comment for clarification
   - Click **Save** to record the result (auto-syncs to Google Sheets)

4. **Search and Filter**
   - Use the keyword search bar to find specific comments or rules quickly

5. **Track and Export**
   - View your progress at the top
   - Export labeled results as a CSV (if enabled)

---

## 📚 Use Cases

- 🧑‍⚖️ Content moderation research
- 🤖 Training datasets for AI models (Toxicity, NLP)
- 📊 Human-in-the-loop annotation tasks
- 🎓 Academic projects in NLP, linguistics, and digital media studies

---

## 🙌 Contributions

Contributions are welcome!  
Please open an issue, suggest features, or submit a pull request.

> See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 License

This project is licensed under the MIT License.  
See [LICENSE](LICENSE) for more info.

---

## ✉️ Contact

Maintainer: [bfiliks](https://github.com/bfiliks)  
For support: Open an [Issue](https://github.com/bfiliks/comment-rule-labeling/issues)
