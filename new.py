import time
import streamlit as st
from pdfminer.high_level import extract_text
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

# Set your Groq API key directly
GROQ_API_KEY = "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"

# Define the chatbot class
class GroqChatbot:
    def __init__(self):
        self.llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama3-70b-8192")

    def get_response(self, user_input):
        # Append the user's input to the conversation history
        st.session_state.conversation_history.append(HumanMessage(user_input))
        
        # Define conversation history
        messages = [
            SystemMessage(
                content="You are a professional career guidance assistant. Provide concise suggestions (under 50 words) on resume improvements, highlighting strengths, weaknesses, and resume score. Stay within career-related topics."
            ),
            *st.session_state.conversation_history[-5:]  # Use only the last 5 messages
        ]
        
        # Get the bot response
        try:
            response = self.llm.invoke(messages)
            bot_response = response.content.strip()
            st.session_state.conversation_history.append(SystemMessage(bot_response))
            return bot_response
        except Exception as e:
            return f"Error: {str(e)}"

# Streamlit UI setup
def main():
    st.title("Resume Analyzer & Career Guidance Assistant")
    st.write("Upload your resume and receive career improvement suggestions.")

    # Initialize session state variables
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    # PDF file uploader
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file:
        extracted_text = extract_text(uploaded_file)
        chatbot = GroqChatbot()
        initial_response = chatbot.get_response(extracted_text)
        st.write(initial_response)

    # Display conversation history
    if st.session_state.conversation_history:
        for msg in st.session_state.conversation_history:
            role = "You" if isinstance(msg, HumanMessage) else "Career Assistant"
            color = "#DCF8C6" if isinstance(msg, HumanMessage) else "#EDEDED"
            st.markdown(f"<div style='background-color: {color}; padding: 10px; border-radius: 10px; margin: 5px;'>{role}: {msg.content}</div>", unsafe_allow_html=True)

    # Input area
    user_input = st.text_input("Your response:")
    if user_input:
        chatbot = GroqChatbot()
        bot_response = chatbot.get_response(user_input)
        st.write(bot_response)

if __name__ == "__main__":
    main()
