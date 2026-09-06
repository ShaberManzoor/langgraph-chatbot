import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

# ************* Utility Function ******************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def new_chat(): 
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    st.session_state['messages'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)
        

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])
        
# ************* SESSION SETUP ******************

if 'messages' not in st.session_state:
    st.session_state['messages'] = []
    
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
    
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []
    
add_thread(st.session_state['thread_id'])

# ************* Sidebar UI ******************

st.sidebar.title('Langgraph Chatbot')
if st.sidebar.button('New Chat'):
    new_chat()
    
st.sidebar.header('My Conversation')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)
        
        temp_messages = []
        
        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role': role, 'content': message.content})
            
        st.session_state['messages'] = temp_messages
        

# ************* Main UI ******************
CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.text(message['content'])
        
user_input = st.chat_input('Type you message')

if user_input:
    
    #storing the chat message
    st.session_state['messages'].append({'role': 'user', 'content': user_input})
    with st.chat_message("user"):
        st.text(user_input)
        
    # res = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    # ai_msg = res['messages'][-1].content

    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= CONFIG,
                stream_mode= 'messages'
            )
        )

    st.session_state['messages'].append({'role': 'assistant', 'content': ai_message})