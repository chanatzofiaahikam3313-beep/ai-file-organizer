import streamlit as st
import google.generativeai as genai

# הגדרת עמוד
st.set_page_config(page_title="AI File Manager", layout="wide")
st.title("📂 מנהל קבצים חכם")

# הגדרות בסידבר
with st.sidebar:
    st.header("הגדרות")
    api_key = st.text_input("הכניסי API Key:", type="password")

if 'history' not in st.session_state:
    st.session_state.history = []

uploaded_file = st.file_uploader("בחרי קובץ")

if uploaded_file and api_key:
    if st.button("🚀 סווג קובץ"):
        try:
            with st.spinner("מנתח..."):
                # הגדרה פשוטה ללא גרסאות בטא
                genai.configure(api_key=api_key)
                
                # שימוש במודל 1.5-flash אבל ללא נתיב ה-models/ המלא שגרם לשגיאה
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # בקשת הסיווג
                prompt = f"Categorize the file name '{uploaded_file.name}' into one Hebrew word. Just the word."
                response = model.generate_content(prompt)
                
                if response.text:
                    category = response.text.strip()
                    st.session_state.history.append({"name": uploaded_file.name, "category": category})
                    st.balloons()
                    st.success(f"הקובץ סווג כ: {category}")
                else:
                    st.error("ה-AI לא החזיר תשובה, נסי שוב.")
                    
        except Exception as e:
            # אם יש שגיאה, ננסה להשתמש במודל הגיבוי באופן אוטומטי
            st.error(f"שגיאה: {e}")
            st.info("מנסה מודל חלופי...")
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                category = response.text.strip()
                st.session_state.history.append({"name": uploaded_file.name, "category": category})
                st.balloons()
            except:
                st.error("לא ניתן להתחבר ל-AI. בדקי את ה-API Key שלך.")

# הצגת היסטוריה
st.markdown("---")
if st.session_state.history:
    st.subheader("היסטוריית סיווג")
    for item in reversed(st.session_state.history):
        st.info(f"📁 **{item['category']}** | {item['name']}")
