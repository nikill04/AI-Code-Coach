"""Web version of AI Code Coach:  streamlit run streamlit_app.py"""
import streamlit as st

from logic import process_query
from prompts import PROMPTS

st.set_page_config(page_title="AI Code Coach", page_icon="🤖", layout="wide")

st.title("🤖 AI Code Coach")
st.markdown("RAG-powered assistant for debugging, translating, and explaining your code.")

# Sidebar
with st.sidebar:
    st.header("Settings")
    task = st.radio("Choose Task:", list(PROMPTS))
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

# Streamlit re-runs this whole file on every click, so the chat is kept in
# st.session_state, which survives between runs.
if "messages" not in st.session_state:
    st.session_state.messages = []


def fix_math(text):
    """The model writes math like \\[ x \\] or \\( x \\), but Streamlit only displays
    math written with $$ x $$ or $ x $. Swap them, leaving code blocks (between ```) alone."""
    parts = text.split("```")
    for i in range(0, len(parts), 2):  # parts 0, 2, 4... are outside code blocks
        parts[i] = (parts[i].replace("\\[", "$$").replace("\\]", "$$")
                            .replace("\\(", "$").replace("\\)", "$"))
    return "```".join(parts)


def show_sources(sources):
    with st.expander("View Context Sources"):
        for source, code in sources:
            st.caption(f"Source: {source}")
            st.code(code, language="python")


# Show the chat so far
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            show_sources(message["sources"])

# Handle a new question
if question := st.chat_input("Ask about your code..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                answer, docs = process_query(task, question)
        except Exception as error:
            st.error(f"Something went wrong: {error}")
            st.stop()

        answer = fix_math(answer)
        sources = [(doc.metadata["source"], doc.page_content) for doc in docs]
        st.markdown(answer)
        show_sources(sources)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )
