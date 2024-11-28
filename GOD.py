import time
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException

# Set your Groq API key directly
GROQ_API_KEY = "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"

# Define the chatbot class
class GroqChatbot:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name="llama-3.1-70b-versatile")

    def get_response(self, user_input):
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
        prompt_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.conversation_history[-5:]])

        # Create a prompt
        prompt = PromptTemplate.from_template(
            f"""
            ### CONVERSATION HISTORY:
            {prompt_text}

            ### INSTRUCTION:
            Respond as an assignment helper for students called as GOD (Guidance On Demand). Provide valid answers assistance based on the conversation history.
            """
        )

        # Retry mechanism for rate limits
        retries = 3
        for attempt in range(retries):
            try:
                result = (prompt | self.llm).invoke({})
                bot_response = result.content.strip()
                st.session_state.conversation_history.append({"role": "GOD", "content": bot_response})
                return bot_response
            except OutputParserException as e:
                return f"Error: {str(e)}"
            except Exception as e:
                if 'Rate limit reached' in str(e):
                    wait_time = 60
                    st.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    return f"Error: {str(e)}"

# Streamlit UI setup
def try():
    st.title("GOD (Guidance On Demand)")
    st.write("Ask your doubts and assignment questions.")

    # Initialize session state
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    # Display conversation history
    for msg in st.session_state.conversation_history:
        if msg['role'] == 'user':
            st.markdown(f"<div style='text-align: right; background-color: #414A4C; padding: 10px; border-radius: 10px;margin: 5px 0;'><strong>You:   </strong>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; background-color: #000000; padding: 10px; border-radius: 10px;margin: 5px 0;'><strong>GOD:   </strong>{msg['content']}</div>", unsafe_allow_html=True)

    # Input field for new messages
    user_input = st.chat_input("Your Response:")
    if user_input:
        chatbot = GroqChatbot()
        bot_response = chatbot.get_response(user_input)
        


try()
