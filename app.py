import streamlit as st

from ocr_pipeline import extract_text_pipeline
from llm_analysis import analyze_with_llm
from vin import extract_vin
from vin_api import fetch_vehicle_details
from chatbot import contract_chatbot


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Car Contract AI Assistant",
    layout="wide"
)

st.title("Car Contract AI Assistant")
st.caption("AI-powered OCR + LLM system for car lease agreement analysis")


# ---------------- SESSION STATE ----------------
if "contract_text" not in st.session_state:
    st.session_state.contract_text = None

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "vin" not in st.session_state:
    st.session_state.vin = None

if "vehicle_details" not in st.session_state:
    st.session_state.vehicle_details = None


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("Upload Contract")

    uploaded_file = st.file_uploader(
        "Upload PDF / Image",
        type=["pdf", "jpg", "jpeg", "png"],
        key="contract_uploader"   # ✅ VERY IMPORTANT
    )

    run_btn = st.button("Run OCR & AI Analysis")


# ---------------- PIPELINE ----------------
if uploaded_file and run_btn:

    # OCR
    with st.spinner("Extracting text using OCR..."):
        contract_text = extract_text_pipeline(uploaded_file)
        st.session_state.contract_text = contract_text

    # LLM Analysis
    with st.spinner("Analyzing contract with AI..."):
        st.session_state.analysis = analyze_with_llm(
            st.session_state.contract_text
        )

    # VIN Extraction
    st.session_state.vin = extract_vin(
        st.session_state.contract_text
    )

    # NHTSA API
    if st.session_state.vin:
        with st.spinner("Fetching vehicle details from NHTSA..."):
            st.session_state.vehicle_details = fetch_vehicle_details(
                st.session_state.vin
            )

    st.success("Analysis completed successfully!")


# ---------------- RESULTS ----------------
col1, col2 = st.columns(2)

with col1:
    if st.session_state.contract_text:
        st.subheader("OCR Extracted Text")
        st.text_area(
            "Contract Text",
            st.session_state.contract_text,
            height=400
        )

with col2:
    if st.session_state.analysis:
        st.subheader("AI Contract Analysis")
        st.write(st.session_state.analysis)


# ---------------- VIN + VEHICLE DETAILS ----------------
if st.session_state.vin:
    st.subheader("VIN Detected")
    st.code(st.session_state.vin)

    if st.session_state.vehicle_details:
        st.subheader("Vehicle Details (NHTSA)")
        if "error" in st.session_state.vehicle_details:
            st.error(st.session_state.vehicle_details["error"])
        else:
            for k, v in st.session_state.vehicle_details.items():
                st.write(f"*{k}:* {v}")


# ---------------- CHATBOT ----------------
if st.session_state.contract_text:
    st.subheader("Ask Questions About the Contract")

    user_query = st.text_input(
        "Ask a question about this contract",
        placeholder="e.g. What is the lease duration? Are there any penalties?"
    )

    if user_query:
        with st.spinner("Thinking..."):
            response = contract_chatbot(
                st.session_state.contract_text,
                user_query
            )
        st.markdown("### Answer")
        st.write(response)