import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI File Manager", layout="wide")
st.title("📂 מנהל קבצים חכם")

with st.sidebar:
    st.header("הגדרות")
    api_key = st.text_input("הכניסי את ה-API Key שלך:", type="password")

if 'history' not in st.session_state:
    st.session_state.history = []

uploaded_file = st.file_uploader("בחרי קובץ מהמחשב")

if uploaded_file and api_key:
    if st.button("🚀 נתחי קובץ"):
        try:
            with st.spinner("ה-AI מנתח..."):
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-pro')
                
                prompt = f"Categorize the file name '{uploaded_file.name}' into one Hebrew word. For example: 'Bills', 'Studies', 'Work'."
                response = model.generate_content(prompt)
                
                category = response.text.strip()
                st.session_state.history.append({"name": uploaded_file.name, "category": category})
                st.balloons()
        except Exception as e:
            st.error(f"שגיאה: {e}")

# תצוגת היסטוריה
st.markdown("---")
if st.session_state.history:
    st.subheader("היסטוריית סיווג")
    for item in reversed(st.session_state.history):
        st.info(f"📁 **{item['category']}** | {item['name']}")
