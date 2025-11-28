import streamlit as st
import requests
import time

# --- Configuration ---
st.set_page_config(
    page_title="AutoDesk Orchestrator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Chat Messages */
    .stChatMessage {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    
    /* User Message Override */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #1f2428; /* Slightly lighter for user */
    }

    /* Header */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Status Indicators */
    .status-dot {
        height: 10px;
        width: 10px;
        background-color: #00d2ff;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
        box-shadow: 0 0 5px #00d2ff;
    }
    
    .status-offline {
        background-color: #ff4b4b;
        box-shadow: 0 0 5px #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("⚡ AutoDesk Orchestrator")
    st.markdown("### Enterprise-Grade Intelligent Support System")

# --- Sidebar ---
with st.sidebar:
    st.header("System Status")
    
    # Poll Server Health
    try:
        health = requests.get("http://localhost:8000/health", timeout=1)
        if health.status_code == 200:
            status = health.json()
            st.markdown(f'<div><span class="status-dot"></span> <strong>Core System:</strong> Online</div>', unsafe_allow_html=True)
            st.markdown("---")
            st.subheader("Active Agents")
            for agent in status.get("agents", []):
                st.code(f"🟢 {agent} Agent")
        else:
            st.markdown(f'<div><span class="status-dot status-offline"></span> <strong>Core System:</strong> Error</div>', unsafe_allow_html=True)
    except:
        st.markdown(f'<div><span class="status-dot status-offline"></span> <strong>Core System:</strong> Offline</div>', unsafe_allow_html=True)
        st.error("Cannot connect to backend server.")

    st.markdown("---")
    st.info(
        "**Architecture:**\n"
        "- **Orchestrator:** LangGraph\n"
        "- **LLM:** Grok (OpenRouter)\n"
        "- **Frontend:** Streamlit\n"
        "- **Backend:** FastAPI"
    )

# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    role = message["role"]
    avatar = "👤" if role == "user" else "⚡"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])

# Input
if prompt := st.chat_input("Describe your issue (e.g., 'Refund invoice INV-1234')..."):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Assistant Response
    with st.chat_message("assistant", avatar="⚡"):
        message_placeholder = st.empty()
        
        try:
            with st.spinner("Orchestrating agents..."):
                # Simulate "thinking" steps for UI effect (optional, but looks cool)
                status_placeholder = st.empty()
                status_placeholder.caption("🔄 Supervisor routing ticket...")
                time.sleep(0.5)
                status_placeholder.caption("🔎 Agent executing tools...")
                
                response = requests.post(
                    "http://localhost:8000/chat", 
                    json={"message": prompt},
                    headers={"Content-Type": "application/json"}
                )
                status_placeholder.empty() # Clear status
                
            if response.status_code == 200:
                data = response.json()
                full_response = data.get("response", "Error: No response.")
                message_placeholder.markdown(full_response)
            else:
                full_response = f"❌ Server Error: {response.status_code}"
                message_placeholder.error(full_response)
                
        except Exception as e:
            full_response = f"❌ Connection Error: {e}"
            message_placeholder.error(full_response)
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
