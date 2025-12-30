import streamlit as st
import google.generativeai as genai

# הגדרת עיצוב העמוד
st.set_page_config(page_title="AI File Manager", layout="wide", initial_sidebar_state="expanded")

st.title("📂 מנהל קבצים חכם")
st.markdown("סווגי את הקבצים שלך בקלות בעזרת בינה מלאכותית")

# סרגל צדדי להגדרות
with st.sidebar:
    st.header("⚙️ הגדרות")
    # הוספת .strip() כדי למנוע שגיאות של רווחים מיותרים במפתח
    raw_api_key = st.text_input("הכניסי Gemini API Key:", type="password")
    api_key = raw_api_key.strip() if raw_api_key else None
    
    if api_key:
        st.success("המפתח הוזן בהצלחה!")
    else:
        st.warning("יש להזין מפתח API כדי להתחיל")

# ניהול היסטוריה
if 'history' not in st.session_state:
    st.session_state.history = []

# ממשק העלאת קבצים
uploaded_file = st.file_uploader("בחרי קובץ מהמחשב", type=['pdf', 'docx', 'txt', 'jpg', 'png', 'xlsx'])

if uploaded_file:
    st.info(f"קובץ נבחר: {uploaded_file.name}")
    
    if st.button("🚀 נתחי וסווג קובץ"):
        if not api_key:
            st.error("❌ חסר מפתח API! אנא הכניסי אותו בסרגל הצד.")
        else:
            try:
                with st.spinner("ה-AI מנתח כעת..."):
                    # הגדרת ה-AI
                    genai.configure(api_key=api_key)
                    
                    # שימוש במודל 1.5-flash המהיר
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # שליחת השאילתה - דגש על תשובה בעברית
                    prompt = f"Categorize the file named '{uploaded_file.name}' into one or two words in Hebrew (e.g., 'חשבונות', 'לימודים', 'עבודה'). Return only the category name."
                    response = model.generate_content(prompt)
                    
                    if response and response.text:
                        category = response.text.strip()
                        # שמירה להיסטוריה
                        st.session_state.history.append({"name": uploaded_file.name, "category": category})
                        st.balloons()
                        st.success(f"הסיווג הושלם: **{category}**")
                    else:
                        st.error("ה-AI לא הצליח להחזיר תשובה. נסי שוב.")
            
            except Exception as e:
                # טיפול בשגיאות נפוצות
                error_msg = str(e)
                if "API_KEY_INVALID" in error_msg:
                    st.error("❌ מפתח ה-API אינו תקין. ודאי שהעתקת אותו נכון.")
                else:
                    st.error(f"אירעה שגיאה: {error_msg}")

# הצגת היסטוריית הסיווגים
st.markdown("---")
if st.session_state.history:
    st.subheader("📊 היסטוריית סיווגים")
    for item in reversed(st.session_state.history):
        with st.expander(f"📁 {item['category']} | {item['name']}"):
            st.write(f"שם הקובץ המלא: {item['name']}")
            st.write(f"קטגוריה שנבחרה: {item['category']}")
else:
    st.write("אין עדיין קבצים שסווגו.")
