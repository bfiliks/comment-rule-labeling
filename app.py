
import streamlit as st
import pandas as pd
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Google Sheets Sync Labeling Tool", layout="wide")

st.title("Comment Rule Labeling Tool (Google Sheets Sync)")

# Annotator login
annotator = st.sidebar.text_input("Enter your name to begin:").strip().lower()
if not annotator:
    st.stop()

# Authenticate and connect to Google Sheet
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("gspread_credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("CommentAnnotations").sheet1  # Replace with your actual sheet name
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Ensure required columns exist
for col in ["label", "flag", "comment", "annotator", "timestamp"]:
    if col not in df.columns:
        df[col] = None if col == "label" else ""

# Progress info
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
    # Locate matching row in full df
    full_index = df[(df["rule_text"] == row["rule_text"]) & (df["text"] == row["text"])].index[0]
    df.at[full_index, "label"] = label
    df.at[full_index, "flag"] = flag
    df.at[full_index, "comment"] = comment
    df.at[full_index, "annotator"] = annotator
    df.at[full_index, "timestamp"] = datetime.datetime.now().isoformat()

    # Push updated row to Google Sheets
    sheet.update(f"C{full_index+2}", str(label))       # label
    sheet.update(f"D{full_index+2}", str(flag))        # flag
    sheet.update(f"E{full_index+2}", comment)          # comment
    sheet.update(f"F{full_index+2}", annotator)        # annotator
    sheet.update(f"G{full_index+2}", df.at[full_index, "timestamp"])  # timestamp

    st.success("Saved to Google Sheets!")
