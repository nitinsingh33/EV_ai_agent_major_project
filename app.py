# entry point for Streamlit app(frontend)
import streamlit as st
import requests

API_URL = "https://ev-ai-agent-major-project.onrender.com"

# Secure API_KEY fetch
try:
    API_KEY = st.secrets["API_KEY"]
except KeyError:
    st.error("API_KEY not found in Streamlit secrets! Please set it in Render → Environment Variables.")
    st.stop()

st.set_page_config(page_title="EV AI Agent", layout="wide")

# ---------------- Sidebar ----------------
st.sidebar.header("Upload Files")
uploaded_files = st.sidebar.file_uploader(
    "Select PDF/CSV files", type=["pdf", "csv"], accept_multiple_files=True
)
category = st.sidebar.selectbox("Category", ["pricing", "strategy", "product", "company", "general"])

if st.sidebar.button("Ingest Files") and uploaded_files:
    files = [("files", (f.name, f.read(), f.type or "application/octet-stream")) for f in uploaded_files]
    resp = requests.post(
        f"{API_URL}/ingest/files",
        files=files,
        data={"category": category},
        headers={"x-api-key": API_KEY}
    )
    if resp.ok:
        st.sidebar.success(f"Ingested: {resp.json()}")
    else:
        try:
            st.sidebar.error(f"Error {resp.status_code}: {resp.json().get('detail', resp.text)}")
        except:
            st.sidebar.error(f"Error {resp.status_code}: {resp.text}")

# ---------------- Chat UI ----------------
st.title("EV AI Agent Chat")
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("category"):
            st.markdown(f"**Category:** `{msg['category']}`")
        if msg.get("citations"):
            st.markdown("**Citations:**")
            for c in msg["citations"]:
                st.markdown(f"- {c.get('filename', 'Unknown')} (p.{c.get('page', 'N/A')})")

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
            try:
                st.error(f"Error {resp.status_code}: {resp.json().get('detail', resp.text)}")
            except:
                st.error(f"Error {resp.status_code}: {resp.text}")

# ---------------- Footer ----------------
st.markdown("""
<hr style="margin-top:2rem; margin-bottom:1rem;">
<div style='text-align:center; color:#666; font-size:0.85rem;'>
    <b>Hero EV AI Agent – Strategy Insights</b><br>
    Confidential · For internal use by Hero MotoCorp Strategy Team only
</div>
""", unsafe_allow_html=True)
