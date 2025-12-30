import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI File Manager", layout="wide")
st.title("📂 בדיקת חיבור AI")

with st.sidebar:
    st.header("הגדרות")
    api_key_input = st.text_input("הכניסי API Key:", type="password")
    api_key = api_key_input.strip()

if st.button("🔍 בדוק חיבור עכשיו"):
    if not api_key:
        st.error("נא להכניס מפתח!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            # בדיקה פשוטה מאוד ללא קובץ
            response = model.generate_content("Hello, respond with the word 'OK'")
            st.success(f"החיבור עובד! ה-AI ענה: {response.text}")
            st.balloons()
        except Exception as e:
            st.error(f"אופס! יש שגיאה בתקשורת: {str(e)}")
            st.info("אם מופיעה שגיאת 'Illegal header', נסי ליצור מפתח חדש לגמרי ב-AI Studio.")

st.markdown("---")
uploaded_file = st.file_uploader("או נסי להעלות קובץ לסיווג:")
if uploaded_file and api_key:
    if st.button("🚀 נתחי קובץ"):
        try:
            with st.spinner("מנסה לתקשר עם גוגל..."):
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Categorize this file name: {uploaded_file.name}. One word in Hebrew."
                response = model.generate_content(prompt)
                st.success(f"סיווג: {response.text}")
        except Exception as e:
            st.error(f"שגיאה בניתוח הקובץ: {e}")
