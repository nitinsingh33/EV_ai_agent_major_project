import streamlit as st
import requests

# --- Minimal & Professional CSS ---
st.markdown("""
    <style>
    /* App background */
    .stApp {
        background-color: #f9f9f9;
    }
    /* Chat message bubbles */
    .stChatMessage {
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.8rem;
        font-size: 1rem;
        line-height: 1.5;
    }
    /* User messages */
    .stChatMessage[data-testid="stChatMessage-user"] {
        background-color: #e8f0fe;
        border: 1px solid #d2e3fc;
    }
    /* Assistant messages */
    .stChatMessage[data-testid="stChatMessage-assistant"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
    }
    /* Input box */
    .stTextInput>div>input {
        border-radius: 6px;
        border: 1px solid #dcdcdc;
        padding: 0.6rem;
        font-size: 1rem;
    }
    /* Buttons */
    .stButton>button {
        border-radius: 6px;
        background: #2563eb;
        color: white;
        font-weight: 500;
        padding: 0.4rem 1rem;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        background: #1d4ed8;
    }
    /* Sidebar */
    .stSidebar {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

API_URL = "https://ev-ai-agent-major-project.onrender.com"
API_KEY = st.secrets.get("API_KEY", "")

st.set_page_config(page_title="EV AI Agent", layout="wide")

# Sidebar
st.sidebar.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=120)
st.sidebar.header("📂 File Upload")
uploaded_files = st.sidebar.file_uploader(
    "Select PDF/CSV files", type=["pdf", "csv"], accept_multiple_files=True
)
category = st.sidebar.selectbox("Category", ["pricing", "strategy", "product", "company", "general"])
if st.sidebar.button("Ingest Files") and uploaded_files:
    files = [("files", (f.name, f.read(), f.type)) for f in uploaded_files]
    resp = requests.post(
        f"{API_URL}/ingest/files",
        files=files,
        data={"category": category},
        headers={"x-api-key": API_KEY}
    )
    if resp.ok:
        st.sidebar.success(f"Ingested: {resp.json()}")
    else:
        st.sidebar.error(f"Error: {resp.text}")

# Main Title
st.markdown("<h2 style='text-align:center; color:#333;'>EV AI Agent Chat</h2>", unsafe_allow_html=True)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("category"):
            st.caption(f"Category: {msg['category']}")
        if msg.get("citations"):
            st.markdown("**Citations:**")
            for c in msg["citations"]:
                st.markdown(f"- {c.get('filename', 'Unknown')} (p.{c.get('page', 'N/A')})")

# Chat input
query = st.chat_input("Ask a question...")
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Thinking..."):
        resp = requests.post(
            f"{API_URL}/chat",
            json={"query": query},
            headers={"x-api-key": API_KEY}
        )
        if resp.ok:
            data = resp.json()
            answer = data.get("answer", "")
            category = data.get("category", "")
            citations = data.get("citations", [])
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "category": category,
                "citations": citations
            })
            with st.chat_message("assistant"):
                st.markdown(answer)
                if category:
                    st.caption(f"Category: {category}")
                if citations:
                    st.markdown("**Citations:**")
                    for c in citations:
                        st.markdown(f"- {c.get('filename', 'Unknown')} (p.{c.get('page', 'N/A')})")
        else:
            st.error(f"Error: {resp.text}")

# Footer
st.markdown(
    "<hr><div style='text-align:center; color:#888; font-size:0.85rem;'>© 2025 EV AI Agent Team</div>",
    unsafe_allow_html=True
)
