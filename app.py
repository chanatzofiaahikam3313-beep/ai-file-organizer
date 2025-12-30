import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI File Manager", layout="wide")
st.title("📂 AI File Manager")

with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key:", type="password")

if 'history' not in st.session_state:
    st.session_state.history = []

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file and api_key:
    if st.button("Analyze with AI"):
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"Suggest one short category for: {uploaded_file.name}")
            category = response.text.strip()
            st.session_state.history.append({"name": uploaded_file.name, "category": category})
            st.success(f"Suggested Category: {category}")
        except:
            st.error("Check your API key.")

st.subheader("History")
for item in reversed(st.session_state.history):
    st.write(f"📁 {item['category']} | {item['name']}")