
# Comment Rule Labeling Tool

A Streamlit-based app to label YouTube comments against community rules. Includes:
- Binary labels (0 = OK, 1 = Violation)
- Comment + Rule pairing
- Flagging
- Annotator notes
- Metadata logging (user, timestamp)

## To run locally:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## To deploy on Streamlit Cloud:
1. Push this repo to GitHub
2. Visit https://streamlit.io/cloud
3. Click 'New App' and link your GitHub repo
