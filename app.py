import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI File Manager", layout="wide")
st.title("📂 מנהל קבצים חכם")

with st.sidebar:
    st.header("הגדרות")
    api_key_input = st.text_input("הכניסי API Key:", type="password")
    api_key = api_key_input.strip()

if 'history' not in st.session_state:
    st.session_state.history = []

uploaded_file = st.file_uploader("בחרי קובץ מהמחשב")

if uploaded_file and api_key:
    if st.button("🚀 סווג קובץ"):
        try:
            with st.spinner("מנתח..."):
                # הגדרת המפתח
                genai.configure(api_key=api_key)
                
                # שימוש במודל היציב ביותר ללא סיומות בטא
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                
                # בקשת הסיווג
                prompt = f"Categorize the file name '{uploaded_file.name}' into one or two words in Hebrew. Return only the category."
                response = model.generate_content(prompt)
                
                # בדיקה שהתקבלה תשובה
                if response.text:
                    category = response.text.strip()
                    st.session_state.history.append({"name": uploaded_file.name, "category": category})
                    st.balloons()
                    st.success(f"הקובץ סווג כ: {category}")
                
        except Exception as e:
            # אם יש שגיאה עם פלאש, ננסה את המודל השני באופן אוטומטי
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                category = response.text.strip()
                st.session_state.history.append({"name": uploaded_file.name, "category": category})
                st.balloons()
                st.success(f"הסיווג הצליח (מודל גיבוי): {category}")
            except:
                st.error(f"שגיאה סופית: {e}")

# תצוגת ההיסטוריה
st.markdown("---")
if st.session_state.history:
    st.subheader("היסטוריית סיווג")
    for item in reversed(st.session_state.history):
        st.info(f"📁 **{item['category']}** | {item['name']}")
