
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

## 🛠 How to Use This Tool

1. **Launch the App**
   - Visit: `https://https://comment-rule-labeling.streamlit.app/`
   - Enter your **annotator name** to begin

2. **Upload CSV File**
   - Format: `rule_text`, `text`, `input`
   - Make sure your data includes paired rules and comments

3. **Label and Annotate**
   - Choose whether the comment violates the rule (0 = No, 1 = Yes)
   - Optionally add a flag or comment
   - All annotations are automatically tagged with your name and timestamp

4. **Search or Filter**
   - Use the search bar to find keywords
   - Filter by specific rules

5. **Export Labeled Data**
   - Click “Download Labeled Data” to save your results as a CSV
