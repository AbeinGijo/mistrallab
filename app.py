import streamlit as st
from helper import classify_intent, generate_reply, summarize_conversation

st.set_page_config(page_title="Bank Support Chatbot (Mistral)", page_icon="💬")

st.title("💬 Bank Customer Support Chatbot (Mistral)")
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False

if not st.session_state.welcome_shown:
    st.info("""
👋 Welcome! I can help you with:
            
• Card delivery issues  
• PIN changes  
• Exchange rates  
• Transfer cancellation  
• Charge disputes  

Try one of the example prompts in the sidebar!
""")
    st.session_state.welcome_shown = True

st.sidebar.title("💡 Example Prompts")

examples = [
    "My card hasn’t arrived yet",
    "I forgot my PIN, how do I change it?",
    "What is the USD to QAR exchange rate?",
    "Can I cancel my pending transfer?",
    "I was charged twice for a payment"
]

selected_example = None
for ex in examples:
    if st.sidebar.button(ex):
        selected_example = ex

with st.sidebar:
    st.subheader("Settings")
    auto_summary = st.toggle("Auto-summarize long chats", value=True)

if "messages" not in st.session_state:
    st.session_state.messages = []  


for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m["role"] == "assistant" and m.get("intent"):
            st.markdown(f"**Detected intent:** `{m['intent']}`")
        st.write(m["content"])

user_text = st.chat_input("Ask: card delivery, PIN, exchange rate, disputes, transfers...")
if selected_example:
    user_text = selected_example

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)
    with st.spinner("🤖 Thinking..."):
        intent = classify_intent(user_text)
        reply = generate_reply(user_text, intent)

    st.session_state.messages.append({"role": "assistant", "content": reply, "intent": intent})
    with st.chat_message("assistant"):
        st.markdown(f"**Detected intent:** `{intent}`")
        st.write(reply)

    if auto_summary:
        convo_text = "\n".join(
            [f"{m['role'].upper()}: {m['content']}" + (f" (intent: {m.get('intent')})" if m.get("intent") else "")
             for m in st.session_state.messages]
        )
        if len(convo_text) > 1200:
            with st.spinner("🧠 Summarizing conversation..."):
                summary = summarize_conversation(convo_text)

            st.info("Conversation Summary")
            st.write(summary)
