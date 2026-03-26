import streamlit as st
import requests

# --- CONFIGURATION ---
GROQ_API_KEY = "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" 

st.set_page_config(page_title="Sama Engineering AI", page_icon="🏗️", layout="centered")

# Custom UI Styling
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        .stChatMessage {border-radius: 15px; margin-bottom: 8px;}
        .stButton>button {width: 100%; border-radius: 20px; background-color: #007bff; color: white;}
    </style>
    """, unsafe_allow_html=True)

st.title("Sama Engineering AI Assistant 🤖")
st.caption("Official Sales Prototype | Karachi, Pakistan")
st.markdown("---")

# 1. Load Knowledge Base
try:
    with open("sama_data.txt", "r", encoding='utf-8') as f:
        context = f.read()
except FileNotFoundError:
    st.error("Error: 'sama_data.txt' not found.")
    st.stop()

# 2. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Chat Logic
if prompt := st.chat_input("Machine ki maloomat ke liye yahan likhein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            
            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {
                        "role": "system", 
                        "content": f"""
ROLE: Official Sales Representative of Sama Engineering (Karachi).
CONTEXT: {context}

STRICT GUIDELINES:
1. CONCISENESS: Be extremely brief. Provide technical specs in short bullet points. Avoid long paragraphs.
2. LANGUAGE: Use Professional English or Pakistani Roman Urdu only.
3. NO HINDI: Strictly ban words like 'Upyukt', 'Jaankari', 'Sampark', 'Adhik'. Use 'Behtareen', 'Maloomat', 'Rabta', 'Zyada'.
4. STRUCTURE: 
   - Acknowledge the machine.
   - List 3-4 key specs/features.
   - Give 1 clear Call to Action (Visit Showroom/Contact).

CONTACT: Nazimabad #2 / Korangi. Phone: +92-300-2449332.
"""
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.0 
            }
            
            response = requests.post(url, json=payload, headers=headers)
            res_data = response.json()

            if 'choices' in res_data:
                reply = res_data['choices'][0]['message']['content']
                with st.chat_message("assistant"):
                    st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception:
            st.error("Connection error.")
