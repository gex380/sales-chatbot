import openai
import streamlit as st
import os

# Secure your key in production! (for now, direct assignment is fine for testing)
openai.api_key = st.secrets["OPENAI_API_KEY"]

def run_chat():
    print("🎯 Welcome to the Sales Training Chatbot!")
    print("This chatbot simulates a real sales conversation in a healthcare setting.")
    print("Your goal is to play the role of a sales representative trying to introduce a new medical software product.")
    print("The bot will act as a potential client — you’ll handle objections, ask questions, and try to guide the conversation.")
    print("After 3 interactions, you'll receive a performance score and feedback.\n")
    print("📝 Type 'exit' at any time to end the simulation.\n")

    print("💡 Example starter questions you can ask the client:")
    print("- What software are you currently using?")
    print("- What are some challenges you're facing with your current system?")
    print("- How satisfied are you with your vendor's support?")
    print("- If there’s one thing you could improve in your system, what would it be?")
    print("- Are you open to exploring new solutions that may better meet your needs?\n")

    messages = [
        {
            "role": "system",
            "content": (
                "You are simulating a realistic healthcare software sales scenario. "
                "Your role is to play the potential client at a hospital or clinic who is being approached by a sales representative (the user). "
                "Do NOT take the role of a salesperson. Wait for the user to begin the conversation and respond as a professional healthcare administrator or department lead evaluating software vendors. "
                "Mention your current provider, raise common objections (vendor loyalty, budget, security), or ask questions about the new solution as appropriate. "
                "Stay in character and do not provide feedback unless explicitly asked."
            )
        }
    ]

    user_turns = 0

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})
        user_turns += 1

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply = response.choices[0].message.content
        print("AI:", reply)
        messages.append({"role": "assistant", "content": reply})

        # After 3 user messages, end and generate feedback
        if user_turns >= 3:
            print("\n--- Generating feedback on your performance... ---\n")
            messages.append({
                "role": "system",
                "content": (
                    "Now that the conversation is complete, evaluate the user's performance in the role of a sales representative. "
                    "Score them out of 10 based on professionalism, handling objections, and persuasiveness. "
                    "Then provide 2–3 specific suggestions for improvement."
                )
            })

            feedback = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            print("Feedback:\n" + feedback.choices[0].message.content)
            break

run_chat()
