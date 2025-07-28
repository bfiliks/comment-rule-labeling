
import streamlit as st
import pandas as pd
import datetime
import io

st.set_page_config(page_title="Comment Rule Labeling Tool", page_icon="favicon.png", layout="wide")

st.title("🧠 Comment Rule Labeling Tool")

# Sidebar Legend
with st.sidebar.expander("📘 How to Use This Tool"):
    st.markdown("""
**Annotator Instructions:**

1. **Enter your annotator name** (used for tracking contributions).
2. **Upload a CSV file** with paired *rules* and *comments*.
3. For each item:
   - Assign a **label**: `0` for NOT violating, `1` for VIOLATING.
   - Optionally **flag** uncertain comments.
   - Leave a **note** if needed.
4. Click **Save** to store your labels.
5. ➕ Use the **plus (+)** button beside the index to move to the next item.
6. Click **Download** to export labeled data at any time.
""")

    st.markdown("[🌐 GitHub Repository](https://github.com/bfiliks/comment-rule-labeling)")

# Annotator login
if 'annotator' not in st.session_state:
    st.session_state.annotator = st.text_input("Enter your annotator name to begin:")
    st.stop()

# Upload CSV
uploaded_file = st.file_uploader("📄 Upload your comment-rule pairs CSV", type="csv")

if uploaded_file and 'csv_data' not in st.session_state:
    st.session_state.csv_data = uploaded_file.read()

if 'csv_data' in st.session_state and 'df' not in st.session_state:
    df = pd.read_csv(io.StringIO(st.session_state.csv_data.decode("utf-8")))
    if 'label' not in df.columns: df['label'] = None
    if 'flag' not in df.columns: df['flag'] = False
    if 'comment' not in df.columns: df['comment'] = ""
    if 'annotator' not in df.columns: df['annotator'] = ""
    if 'timestamp' not in df.columns: df['timestamp'] = ""
    st.session_state.df = df

if 'df' in st.session_state:
    df = st.session_state.df

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
        st.session_state.df = df
        st.success("Saved successfully.")

    # Progress bar
    total = len(df)
    completed = df['label'].notna().sum()
    progress = completed / total if total > 0 else 0
    st.progress(progress)
    st.markdown(f"**Progress:** {completed} out of {total} labeled ({progress:.0%})")

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download labeled data", csv, "labeled_output.csv", "text/csv")

    st.markdown("---")
    st.write(f"✅ Labeled: {completed} / {total}")
