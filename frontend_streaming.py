import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {'configurable': {'thread_id': 1}}

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.text(message['content'])
        
user_input = st.chat_input('Type you message')

if user_input:
    
    #storing the chat message
    st.session_state['messages'].append({'role': 'user', 'content': user_input})
    with st.chat_message("user"):
        st.text(user_input)
        
    res = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    ai_msg = res['messages'][-1].content

    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= {'configurable': {'thread_id': 'thread-1'}},
                stream_mode= 'messages'
            )
        )

    st.session_state['messages'].append({'role': 'assistant', 'content': ai_message})