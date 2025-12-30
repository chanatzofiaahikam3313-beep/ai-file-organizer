import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI File Manager", layout="wide")
st.title("📂 AI File Manager")

with st.sidebar:
    st.header("הגדרות")
    api_key = st.text_input("הכניסי את ה-API Key שלך:", type="password")

if 'history' not in st.session_state:
    st.session_state.history = []

uploaded_file = st.file_uploader("בחרי קובץ")

if uploaded_file and api_key:
    if st.button("🚀 נתחי עם AI"):
        try:
            with st.spinner("ה-AI מנתח את הקובץ..."):
                genai.configure(api_key=api_key)
                # משתמשים ב-gemini-pro כי הוא הכי יציב כרגע
                model = genai.GenerativeModel('gemini-pro')
                
                prompt = f"Categorize the file name '{uploaded_file.name}' into one Hebrew word. Just the word."
                response = model.generate_content(prompt)
                
                category = response.text.strip()
                st.session_state.history.append({"name": uploaded_file.name, "category": category})
                st.balloons()
        except Exception as e:
            st.error(f"שגיאה: {e}")

# תצוגת ההיסטוריה
st.markdown("---")
st.subheader("היסטוריית סיווג")
for item in reversed(st.session_state.history):
    st.info(f"📁 **{item['category']}** | {item['name']}")
