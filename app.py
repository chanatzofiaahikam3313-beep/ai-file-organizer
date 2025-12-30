import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI File Manager", layout="wide")
st.title("📂 AI File Manager")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key:", type="password")

if 'history' not in st.session_state:
    st.session_state.history = []

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file and api_key:
    if st.button("🚀 Analyze"):
        try:
            with st.spinner("Processing..."):
                genai.configure(api_key=api_key)
                
                # שינוי למודל היציב ביותר שתמיד עובד בכל הגרסאות
                model = genai.GenerativeModel('gemini-pro')
                
                prompt = f"Categorize the file name '{uploaded_file.name}' into one Hebrew word."
                response = model.generate_content(prompt)
                
                category = response.text.strip()
                st.session_state.history.append({"name": uploaded_file.name, "category": category})
                st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")

# תצוגת ההיסטוריה
st.markdown("---")
for item in reversed(st.session_state.history):
    st.info(f"📁 {item['category']} | {item['name']}")
