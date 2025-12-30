import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI File Manager", layout="wide")
st.title("📂 AI File Manager (Fast Mode)")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    if api_key:
        st.success("API Key stored!")
    else:
        st.warning("Please enter API Key")

if 'history' not in st.session_state:
    st.session_state.history = []

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file:
    st.info(f"File selected: {uploaded_file.name}")
    
    if st.button("🚀 Analyze & Categorize"):
        if not api_key:
            st.error("❌ Missing API Key!")
        else:
            try:
                with st.spinner("AI is thinking fast..."):
                    genai.configure(api_key=api_key)
                    # שימוש במודל ה-Flash המהיר
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # בקשה ממוקדת לקטגוריה בעברית
                    prompt = f"Identify the category of this file based on its name: '{uploaded_file.name}'. Answer with only one or two words in Hebrew."
                    response = model.generate_content(prompt)
                    
                    category = response.text.strip()
                    st.session_state.history.append({"name": uploaded_file.name, "category": category})
                    st.balloons()
                    st.success(f"סווג בהצלחה: **{category}**")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.subheader("📊 היסטוריית סיווג")
if st.session_state.history:
    for item in reversed(st.session_state.history):
        st.write(f"📁 **{item['category']}** | {item['name']}")
else:
    st.info("אין קבצים שסווגו עדיין.")
