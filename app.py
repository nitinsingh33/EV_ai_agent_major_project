import streamlit as st
import requests

# --- Custom CSS for blur and modern UI ---
st.markdown("""
    <style>
    body {
        background: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1500&q=80') no-repeat center center fixed;
        background-size: cover;
    }
    .stApp {
        background: rgba(255,255,255,0.7);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        min-height: 100vh;
    }
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        background: rgba(255,255,255,0.85);
    }
    .stTextInput>div>input {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 0.75rem;
        font-size: 1.1rem;
    }
    .stButton>button {
        border-radius: 8px;
        background: #0072ff;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background: #0052cc;
    }
    .stSidebar {
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(6px);
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    </style>
""", unsafe_allow_html=True)

API_URL = "https://ev-ai-agent-major-project.onrender.com"
API_KEY = st.secrets.get("AIzaSyB1WbRxcGG-BlaFiBkhQTw7h9PVyBXKVm4", "")

st.set_page_config(page_title="EV AI Agent", layout="wide")

st.sidebar.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=120)
st.sidebar.header("Upload Files")
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

st.markdown("<h1 style='text-align:center;'>🚗 EV AI Agent Chat</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f"<div style='font-size:1.1rem;'>{msg['content']}</div>", unsafe_allow_html=True)
        if msg.get("category"):
            st.markdown(f"<span style='background:#e0e7ff;padding:4px 12px;border-radius:8px;font-weight:500;'>Category: {msg['category']}</span>", unsafe_allow_html=True)
        if msg.get("citations"):
            st.markdown("<b>Citations:</b>", unsafe_allow_html=True)
            for c in msg["citations"]:
                st.markdown(f"- <span style='color:#0072ff;'>{c.get('filename', 'Unknown')} (p.{c.get('page', 'N/A')})</span>", unsafe_allow_html=True)

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
                st.markdown(f"**Category:** `{category}`")
                if citations:
                    st.markdown("**Citations:**")
                    for c in citations:
                        st.markdown(f"- {c.get('filename', 'Unknown')} (p.{c.get('page', 'N/A')})")
        else:
            st.error(f"Error: {resp.text}")

st.markdown("""
    <hr>
    <div style='text-align:center; color: #888; font-size: 0.9rem;'>
        © 2025 EV AI Agent Team
    </div>
""", unsafe_allow_html=True)