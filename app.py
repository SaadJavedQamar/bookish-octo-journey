import streamlit as st
import requests

# --- CONFIGURATION ---
# Yahan apni Groq API Key paste kar dein
GROQ_API_KEY = "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" 

# Page Configuration
st.set_page_config(page_title="Sama Engineering AI Assistant", page_icon="🏗️", layout="centered")

# Custom Styling to hide Sidebar and make it look professional
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        .main {background-color: #f5f7f9;}
        .stChatMessage {border-radius: 15px;}
    </style>
    """, unsafe_allow_html=True)

st.title("Sama Engineering AI Assistant 🤖")
st.caption("Official Prototype for Machine Inquiries - Powered by Llama 3.1")
st.markdown("---")

# 1. Load Knowledge Base
try:
    with open("sama_data.txt", "r") as f:
        context = f.read()
except FileNotFoundError:
    st.error("Error: 'sama_data.txt' file not found. Please create it first.")
    st.stop()

# 2. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Chat Input & AI Logic
if prompt := st.chat_input("Ask about Sama Engineering machines..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Processing
    with st.spinner("Sama AI is typing..."):
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {
                        "role": "system", 
                        "content": f"""
                        Identity: Official AI Sales Representative of Sama Engineering (Karachi).
                        Data: {context}
                        STRICT RULES:
                        1. Respond ONLY in professional, formal English.
                        2. Never use Urdu, Hindi, or Roman Urdu in the output.
                        3. If asked for contact details, provide the Phone, Email, and Karachi address from the data.
                        4. Encourage the user to visit the showroom or book a live demo.
                        """
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2
            }
            
            response = requests.post(url, json=payload, headers=headers)
            res_data = response.json()

            if 'choices' in res_data:
                reply = res_data['choices'][0]['message']['content']
                with st.chat_message("assistant"):
                    st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            else:
                st.error("AI Service is currently busy. Please try again.")
        except Exception as e:
            st.error("Connection error. Please check your internet.")
