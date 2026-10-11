import os
import streamlit as st

# Read the API key from Streamlit Cloud Secrets
try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except Exception:
    pass

from core import analyze_paper

st.set_page_config(page_title="🔬Research Paper Analyzer", layout="centered")

st.title("Research Paper Analyzer")

paper_text = st.text_area("Paper text", height=300)

if st.button("Analyze"):
    if not paper_text.strip():
        st.warning("Please paste the research paper text.")
    else:
        with st.spinner("Analyzing..."):
            try:
                data = analyze_paper(paper_text)
            except Exception as e:
                st.error(f"Could not analyze the paper: {e}")
                st.stop()

        def show_text(label, value):
            st.subheader(label)
            st.write(value if value else "Not mentioned")

        def show_list(label, items):
            st.subheader(label)
            if items:
                for item in items:
                    st.markdown(f"- {item}")
            else:
                st.write("Not mentioned")

        show_text("Title", data.title)
        show_list("Authors", data.authors)
        show_text("Problem Statement", data.problem_statement)
        show_list("Methodology", data.methodology)
        show_list("Algorithms", data.algorithms)
        show_text("Dataset", data.dataset)
        show_text("Results", data.results)
        show_list("Limitations", data.limitations)
        show_text("Research Gap", data.research_gap)
        show_list("Future Work", data.future_work)
