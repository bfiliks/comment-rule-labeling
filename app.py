import streamlit as st
import pandas as pd
import gspread
import json
import datetime
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Comment Rule Labeling Tool", page_icon="favicon.png", layout="wide")
st.title("🧠 Comment Rule Labeling Tool (Google Sheets Sync)")

# --- Sidebar Instructions ---
with st.sidebar.expander("📝 Annotator Instructions", expanded=True):
    st.markdown("""
    ### 👋 Welcome, Annotator!

    Use this tool to **label** YouTube comments based on specific community rules.

    #### 📌 Steps to Begin:
    1. **Enter your name** below.
    2. The app loads data from a shared Google Sheet.
    3. For each comment:
       - Label:  
         `0` → Not Violating  
         `1` → Violates Rule
       - Optional: Flag 🚩 and Comment 💬
    4. Click “Save”.
    5. Manually navigate rows using the + / - control.

    #### 🛠️ Tips:
    - Use the “Download Labeled Data” at the bottom to export your progress.
    - All updates are synced in real-time with timestamp and name.

    🔍 Need help? [GitHub Support](https://github.com/bfiliks/comment-rule-labeling/issues)
    """)

# --- Login ---
annotator = st.sidebar.text_input("Enter your name to begin:").strip().lower()
if not annotator:
    st.stop()

# --- Auth and Load from Google Sheets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
gspread_dict = json.loads(st.secrets["gspread_credentials"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(gspread_dict, scope)
client = gspread.authorize(creds)

sheet = client.open("CommentAnnotations").sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)

# --- Ensure columns exist ---
for col in ["label", "flag", "comment", "annotator", "timestamp"]:
    if col not in df.columns:
        df[col] = None if col == "label" else ""

# --- Track Progress ---
total = len(df)
completed = df["label"].notna().sum()
progress = completed / total if total else 0

st.progress(progress)
st.markdown(f"**Progress:** {completed} / {total} labeled")

# --- Filter for unlabeled rows ---
filtered = df[df["label"].isna()].reset_index(drop=True)
if filtered.empty:
    st.success("🎉 All comments have been labeled!")
    st.stop()

# --- Current Index ---
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

# --- Save Logic ---
if st.button("💾 Save"):
    # Find matching full row index
    matches = df[(df["rule_text"] == row["rule_text"]) & (df["text"] == row["text"])]
    if matches.empty:
        st.error("Could not match row in full dataset. Skipping save.")
    else:
        full_index = matches.index[0]
        timestamp = datetime.datetime.now().isoformat()

        df.at[full_index, "label"] = label
        df.at[full_index, "flag"] = flag
        df.at[full_index, "comment"] = comment
        df.at[full_index, "annotator"] = annotator
        df.at[full_index, "timestamp"] = timestamp

        sheet.update(f"C{full_index+2}", str(label))       # label
        sheet.update(f"D{full_index+2}", str(flag))        # flag
        sheet.update(f"E{full_index+2}", comment)          # comment
        sheet.update(f"F{full_index+2}", annotator)        # annotator
        sheet.update(f"G{full_index+2}", timestamp)        # timestamp

        st.success("✅ Saved to Google Sheets!")
