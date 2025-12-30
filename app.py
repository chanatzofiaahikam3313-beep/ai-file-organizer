import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI File Manager", layout="wide")
st.title("📂 AI File Manager")

# סרגל צדדי להגדרות
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    if api_key:
        st.success("API Key stored!")
    else:
        st.warning("Please enter API Key to start")

if 'history' not in st.session_state:
    st.session_state.history = []

# ממשק ראשי
uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'txt', 'jpg', 'png'])

if uploaded_file:
    st.info(f"File selected: {uploaded_file.name}")
    
    if st.button("🚀 Analyze & Categorize"):
        if not api_key:
            st.error("❌ Missing API Key! Please paste it in the sidebar on the left.")
        else:
            try:
                with st.spinner("AI is thinking..."):
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-pro')
                    
                    # בקשה מה-AI
                    prompt = f"Identify the category of this file based on its name: '{uploaded_file.name}'. Answer with only one or two words (the category)."
                    response = model.generate_content(prompt)
                    
                    category = response.text.strip()
                    st.session_state.history.append({"name": uploaded_file.name, "category": category})
                    st.balloons() # חגיגה קטנה כשזה מצליח
                    st.success(f"Done! Category: **{category}**")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# הצגת היסטוריה
st.markdown("---")
st.subheader("📊 Classification History")
if st.session_state.history:
    for item in reversed(st.session_state.history):
        st.write(f"📁 **{item['category']}** | {item['name']}")
else:
    st.info("No files categorized yet.")
