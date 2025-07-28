
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Comment Rule Labeling Tool", page_icon="favicon.png", layout="wide")

st.title("🧠 Comment Rule Labeling Tool")

# 👋 Welcome Message
st.markdown("""
### 👋 Welcome, Annotators!

This tool helps you **label, flag, and comment on YouTube comments** based on specific community rules.

Please follow the steps below to begin:
1. **Enter your annotator name** when prompted (this helps log your inputs).
2. **Upload your CSV file** containing paired *rules* and *comments*.
3. For each comment:
   - Assign a **label**: `0` (not violating) or `1` (violates the rule).
   - Optionally **flag** uncertain cases and leave a **note** for review.
4. Use the **“Download Labeled Data”** button to export your progress.

---

Need help? Reach out to the team or [open an issue](https://github.com/bfiliks/comment-rule-labeling/issues).
""")

# --- USER LOGIN ---
if 'annotator' not in st.session_state:
    st.sidebar.markdown("[🔗 View on GitHub](https://github.com/bfiliks/comment-rule-labeling)")
    st.session_state.annotator = st.text_input("Enter your annotator name to begin:")
    st.stop()

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("📄 Upload your comment-rule pairs CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'label' not in df.columns: df['label'] = None
    if 'flag' not in df.columns: df['flag'] = False
    if 'comment' not in df.columns: df['comment'] = ""
    if 'annotator' not in df.columns: df['annotator'] = ""
    if 'timestamp' not in df.columns: df['timestamp'] = ""

    search_term = st.text_input("🔍 Search in comments or rules:")
    filtered = df[df['text'].str.contains(search_term, case=False, na=False) | df['rule_text'].str.contains(search_term, case=False, na=False)] if search_term else df

    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0

    index = st.number_input("Index", min_value=0, max_value=len(filtered)-1, value=st.session_state.current_index)
    st.session_state.current_index = index
    row = filtered.iloc[index]

    st.subheader("📌 Rule")
    st.info(row['rule_text'])

    st.subheader("💬 Comment")
    st.warning(row['text'])

    label = st.radio("Label", [0, 1], index=0 if row['label'] != 1 else 1, horizontal=True)
    flag = st.checkbox("🚩 Flag this data?", value=row['flag'])
    note = st.text_area("💬 Comment (optional)", value=row['comment'])

    if st.button("💾 Save"):
        row_index = row.name
        df.at[row_index, 'label'] = label
        df.at[row_index, 'flag'] = flag
        df.at[row_index, 'comment'] = note
        df.at[row_index, 'annotator'] = st.session_state.annotator
        df.at[row_index, 'timestamp'] = datetime.datetime.now().isoformat()
        st.success("Saved successfully.")

        # 🚀 Auto-advance to next index
        if st.session_state.current_index < len(filtered) - 1:
            st.session_state.current_index += 1
            st.experimental_rerun()

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download labeled data", csv, "labeled_output.csv", "text/csv")

    st.markdown("---")
    st.write(f"✅ Labeled: {df['label'].notna().sum()} / {len(df)}")
