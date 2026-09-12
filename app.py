import streamlit as st
from main import detect_errors, explain_error


st.set_page_config(
    page_title="SobanPy",
    page_icon="🐍",
    layout="wide"
)


# Header
st.title("SobanPy")
st.caption("Python Error Detector & AI Explanation Tool")

st.markdown("""
**Created by Muhammad Soban**  
🎓 BS Software Engineering • 🏫 NFC-IET Multan • 🇵🇰 Pakistan
""")

st.divider()


# Python code input
st.subheader("💻 Python Code")

code = st.text_area(
    "Write or paste your Python code below:",
    height=350,
    placeholder='Example:\nname = "Soban"\nprint(name)'
)


# Analyze button
if st.button("🔍 Analyze Code", type="primary"):

    if not code.strip():

        st.warning("⚠️ Please enter some Python code.")

    else:

        errors = detect_errors(code)

        if errors:

            st.subheader("🚨 Error Detected")

            for error in errors:

                st.error(
                    f'{error["error_type"]} — Line {error["line"]}'
                )

                st.write(
                    f'**Error message:** {error["message"]}'
                )

                st.markdown("### 🤖 AI Explanation")

                with st.spinner("Gemini is analyzing the error..."):

                    explanation = explain_error(error)

                st.info(explanation)

        else:

            st.success("✅ No errors detected!")

            st.balloons()
