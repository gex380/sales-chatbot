import streamlit as st
import openai

# Load OpenAI API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Healthcare Sales Chatbot")
st.title("🤖 Sales Training Chatbot for Healthcare Reps")

st.markdown("""
Welcome to the **AI-powered sales training chatbot**.  
You're the sales rep — the bot is the potential client.  
After 3 messages, you'll receive a score and coaching feedback.

💡 **Starter questions you can try:**
- What software are you currently using?
- What challenges are you facing?
- How satisfied are you with your current system?
- Are you open to a better solution?
""")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are simulating a realistic healthcare software sales scenario. "
                "Your role is to play the potential client at a hospital or clinic who is being approached by a sales representative (the user). "
                "Do NOT take the role of a salesperson. Wait for the user to begin the conversation and respond as a professional healthcare administrator. "
                "Mention your current provider, raise objections (vendor loyalty, budget), or ask questions. Stay in character."
            )
        }
    ]
    st.session_state.user_turns = 0
    st.session_state.feedback_given = False

# Display chat history
for msg in st.session_state.messages[1:]:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# Chat input box
if not st.session_state.feedback_given:
    user_input = st.chat_input("Type your message here...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.user_turns += 1

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("AI is thinking..."):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.markdown(reply)

        # Trigger feedback after 3 user turns
        if st.session_state.user_turns >= 3:
            st.session_state.feedback_given = True

            st.session_state.messages.append({
                "role": "system",
                "content": (
                    "Now evaluate the user's performance in the role of a sales rep. "
                    "Score them out of 10 based on professionalism, objection handling, and clarity. "
                    "Then provide 2–3 improvement suggestions."
                )
            })

            with st.spinner("Analyzing your performance..."):
                feedback = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages
                )
                feedback_text = feedback.choices[0].message.content

            st.markdown("---")
            st.subheader("📊 Sales Performance Feedback")
            st.success(feedback_text)

# Reset button
if st.button("🔄 Start Over"):
    for key in ["messages", "user_turns", "feedback_given"]:
        st.session_state.pop(key, None)
    st.experimental_rerun()
