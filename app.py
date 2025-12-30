import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="מנהל קבצים", layout="wide")
st.title("📂 מנהל קבצים חכם")

with st.sidebar:
    st.header("הגדרות")
    api_key_input = st.text_input("הכניסי API Key חדש:", type="password")
    api_key = api_key_input.strip()

if 'history' not in st.session_state:
    st.session_state.history = []

uploaded_file = st.file_uploader("בחרי קובץ")

if uploaded_file and api_key:
    if st.button("🚀 סווג קובץ"):
        try:
            with st.spinner("מתחבר לבינה המלאכותית..."):
                genai.configure(api_key=api_key)
                
                # שימוש בשם המודל הבסיסי ביותר כדי למנוע שגיאות גרסה
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"Categorize the file '{uploaded_file.name}' into one Hebrew word like 'Bills', 'Work', 'Studies'."
                response = model.generate_content(prompt)
                
                if response.text:
                    category = response.text.strip()
                    st.session_state.history.append({"name": uploaded_file.name, "category": category})
                    st.balloons()
                
        except Exception as e:
            # אם יש שגיאה, נציג אותה בצורה ברורה
            st.error(f"עדיין יש בעיה במפתח: {e}")
            st.info("ודאי שהשתמשת במפתח שנוצר ב-'New Project'.")

# תצוגת היסטוריה
st.markdown("---")
for item in reversed(st.session_state.history):
    st.info(f"📁 **{item['category']}** | {item['name']}")
