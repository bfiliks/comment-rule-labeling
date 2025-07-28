
import streamlit as st
import pandas as pd
import datetime
import io

st.set_page_config(page_title="Multi-Annotator Comment Rule Labeling Tool", page_icon="🧠", layout="wide")

st.title("🧠 Multi-Annotator Comment Rule Labeling Tool")

# Sidebar Instructions
with st.sidebar.expander("📘 Annotator Instructions"):
    st.markdown("""
**How to Use:**

1. Enter your **annotator name** (e.g., `alice`, `bob`, `carla`).
2. Upload the shared CSV.
3. You will **only see rows you haven't labeled**.
4. Label each comment as `0` (not violating) or `1` (violates the rule).
5. Optionally **flag** or **comment**.
6. Click **Save** and use the **+** to go to the next item.
7. Click **Download** to save your progress.

🧠 Other annotators' labels are tracked in separate columns.
""")

# Annotator login
annotator = st.sidebar.text_input("Enter your annotator name (e.g., alice, bob, carla):").strip().lower()
if not annotator:
    st.stop()

# Upload file
uploaded_file = st.file_uploader("📄 Upload shared comment-rule CSV", type="csv")

if uploaded_file and 'csv_data' not in st.session_state:
    st.session_state.csv_data = uploaded_file.read()

if 'csv_data' in st.session_state and 'df' not in st.session_state:
    df = pd.read_csv(io.StringIO(st.session_state.csv_data.decode("utf-8")))

    for col in [f'label_{annotator}', f'flag_{annotator}', f'comment_{annotator}', f'timestamp_{annotator}']:
        if col not in df.columns:
            if 'label' in col:
                df[col] = None
            elif 'flag' in col:
                df[col] = False
            else:
                df[col] = ""
    st.session_state.df = df

if 'df' in st.session_state:
    df = st.session_state.df

    # Filter to rows this annotator hasn't labeled yet
    filtered = df[df[f'label_{annotator}'].isna()].reset_index(drop=True)

    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0

    if filtered.empty:
        st.success("🎉 All comments have been labeled by you!")
    else:
        index = st.number_input("Index", min_value=0, max_value=len(filtered)-1, value=st.session_state.current_index)
        st.session_state.current_index = index
        row = filtered.iloc[index]

        st.subheader("📌 Rule")
        st.info(row['rule_text'])

        st.subheader("💬 Comment")
        st.warning(row['text'])

        label = st.radio("Label", [0, 1], horizontal=True)
        flag = st.checkbox("🚩 Flag this data?")
        note = st.text_area("💬 Comment (optional)")

        if st.button("💾 Save"):
            full_index = df[(df['rule_text'] == row['rule_text']) & (df['text'] == row['text'])].index[0]
            df.at[full_index, f'label_{annotator}'] = label
            df.at[full_index, f'flag_{annotator}'] = flag
            df.at[full_index, f'comment_{annotator}'] = note
            df.at[full_index, f'timestamp_{annotator}'] = datetime.datetime.now().isoformat()
            st.session_state.df = df
            st.success("Saved successfully!")

        total = len(df)
        completed = df[f'label_{annotator}'].notna().sum()
        progress = completed / total if total else 0
        st.progress(progress)
        st.markdown(f"**Progress:** {completed} / {total} labeled by `{annotator}`")

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download your labeled CSV", csv, f"{annotator}_labeled_output.csv", "text/csv")
