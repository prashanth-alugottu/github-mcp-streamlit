import streamlit as st
import asyncio
from agent import run_agent_async

# Page configuration
st.set_page_config(
    page_title="MCP AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        padding-top: 0rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 MCP AI Agent - GitHub")
st.markdown(
    "<small>Use this tool to connect, explore, and manage GitHub repositories or local files seamlessly through MCP servers.</small>",
    unsafe_allow_html=True
)
st.markdown("---")
# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "loading" not in st.session_state:
    st.session_state.loading = False

# Display chat history
st.subheader("Conversation")
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
st.markdown("---")
user_input = st.chat_input("Enter your request to the AI Agent...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Display user message
    with chat_container:
        with st.chat_message("user"):
            st.markdown(user_input)
    
    # Show loading state
    with st.spinner("🔄 Agent is processing your request..."):
        try:
            # Call async agent function
            response = asyncio.run(run_agent_async(user_input))
            
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            
            # Display assistant response
            with chat_container:
                with st.chat_message("assistant"):
                    st.markdown(response)
        except Exception as e:
            error_message = f"❌ Error: {str(e)}"
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message
            })
            
            with chat_container:
                with st.chat_message("assistant"):
                    st.error(error_message)

# Sidebar for app info
with st.sidebar:
    st.header("📋 About")
    st.markdown("""
    This AI Agent can:
    - 📁 **Browse and manage files** via Filesystem MCP
    - 🐙 **Interact with GitHub** via GitHub MCP
    - 🤖 **Execute tasks** using GPT-4o-mini
    
    **Capabilities:**
    - Read/write files
    - Create directories
    - GitHub repository operations
    - Code analysis
    """)
    
    st.markdown("---")
    st.header("🔧 Configuration")
    
    if st.session_state.messages:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    message_count = len([m for m in st.session_state.messages if m["role"] == "user"])
    st.metric("Total Messages", message_count)
