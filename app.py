
import streamlit as st
import pandas as pd
import gspread
import json
import datetime
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Google Sheets Sync Labeling Tool", page_icon="favicon.png", layout="wide")
st.title("Comment Rule Labeling Tool")

# Annotator Sidebar Instructions
with st.sidebar.expander("📝 Annotator Instructions", expanded=True):
    st.markdown("""
    ### 👋 Welcome, Annotator!

    Use this tool to **label** YouTube comments based on specific subreddit or community rules.

    #### 📌 Steps to Begin:
    1. **Enter your name** at login (this is recorded for auditing).
    2. **Upload the CSV file** with rule-comment pairs.
    3. For each pair:
       - Assign a label:  
         `0` → **Not Violating**  
         `1` → **Violates Rule**
       - Optionally check **🚩 Flag** if unsure.
       - Leave a **comment** if helpful for others.
    4. **Click “Save”** after labeling.
    5. **Use the + / - buttons** (top center) to manually go to the **next or previous row**.

    #### 📤 Export:
    - Use **Download Labeled Data** at the bottom to save your work as a CSV.
    - All changes are saved with:
      - Your name
      - Timestamp
      - Optional flags and notes

    ---
    🔍 You can search keywords in rules or comments using the search bar.

    🛠️ Need help? [Open an issue on GitHub](https://github.com/bfiliks/comment-rule-labeling/issues)
    """)


# Annotator login
annotator = st.sidebar.text_input("Enter your name to begin:").strip().lower()
if not annotator:
    st.stop()

# Load credentials from Streamlit Secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
gspread_dict = json.loads(st.secrets["gspread_credentials"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(gspread_dict, scope)
client = gspread.authorize(creds)

# Connect to Google Sheet
sheet = client.open("CommentAnnotations").sheet1  # Adjust name if needed
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Ensure required columns exist
for col in ["label", "flag", "comment", "annotator", "timestamp"]:
    if col not in df.columns:
        df[col] = None if col == "label" else ""

# Progress tracking
filtered = df[df["label"].isna()].reset_index(drop=True)
total = len(df)
completed = df["label"].notna().sum()
progress = completed / total if total else 0
st.progress(progress)
st.markdown(f"**Progress:** {completed} / {total} labeled")

if filtered.empty:
    st.success("🎉 All comments have been labeled!")
    st.stop()

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

index = st.number_input("Index", min_value=0, max_value=len(filtered)-1, value=st.session_state.current_index)
st.session_state.current_index = index

row = filtered.iloc[index]
st.subheader("📌 Rule")
st.info(row["rule_text"])

st.subheader("💬 Comment")
st.warning(row["text"])

label = st.radio("Label", [0, 1], horizontal=True)
flag = st.checkbox("🚩 Flag this data?")
comment = st.text_area("💬 Comment (optional)")

if st.button("💾 Save"):
    full_index = df[(df["rule_text"] == row["rule_text"]) & (df["text"] == row["text"])].index[0]
    df.at[full_index, "label"] = label
    df.at[full_index, "flag"] = flag
    df.at[full_index, "comment"] = comment
    df.at[full_index, "annotator"] = annotator
    df.at[full_index, "timestamp"] = datetime.datetime.now().isoformat()

    sheet.update(f"C{full_index+2}", str(label))       # label
    sheet.update(f"D{full_index+2}", str(flag))        # flag
    sheet.update(f"E{full_index+2}", comment)          # comment
    sheet.update(f"F{full_index+2}", annotator)        # annotator
    sheet.update(f"G{full_index+2}", df.at[full_index, "timestamp"])  # timestamp

    st.success("Saved to Google Sheets!")
