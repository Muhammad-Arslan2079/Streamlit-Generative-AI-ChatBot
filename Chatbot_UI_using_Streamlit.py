# importing environment variable to access llm using our api
from dotenv import load_dotenv
import streamlit as st # importing streamlit for ui
from langchain_groq import ChatGroq # importing groq llm/chat class
# loading environment variables
# load_dotenv('Generative AI development/.env') use when both main code and environment file are in different folder then provide path
# if both are in same folder then
load_dotenv()

# streamlit page setup
st.set_page_config(
    page_title='💬 ChatBot',
    page_icon='🤖',
    layout='centered'
)
st.title('🤖  Generative AI ChatBot')
# run: 'streamlit run Chatbot_UI_using_Streamlit.py' path  in terminal to check UI
# chatbox code
#initiate chat history
# we cant just use chat_history object by passing messages as role,content in list
# because streamlit has rule the on every click/interaction the complete code reruns and variables get reset ,but we need previous messages of chat for context
# to deal with this issue we use st.session_state in streamlit that act like a temporary memory and retains data till the app is used by user
# its like a key value pair where chat_history variable is key and its messages in it are its values
# how to use it?
if 'chat_history' not in st.session_state: # first checks if the variable chat_history is already in session memory as a key  pair?
    st.session_state.chat_history=[] # if key is not present means condition is true then empty list will be created
    # then second time the user message will be appended in this empty list using .append
    # but if chat_history key value pair already exist in session history at first then condition will be false and 2nd line will be ignored and no empty list will be created
# 'chat_history' in string in first line act as key name in key-value pair, means check if this key is present?
# key 'chat history' present in what? means present in session_state object which is an object that contains keyvalue pair and serves as temporary memory
# now if condition is true and key is not present then simply a key with name as 'chat history ' will be created
# and the value of this key is an empty list[] in which we will append messages later
# show chat history on the screen, like gpt showing users messages and llm response
for message in st.session_state.chat_history: # for loop runs for one by one message in chat history user,assistant,then again user,then assistan
    with st.chat_message(message['role']): #st.chat message  function will create a box on the right side of screen for user message like in gpt/whatsapp, for assistant message a box will e created on left side of screen for assistant message
        # with simply means that message and content will go inside the box and displayed
        st.markdown(message['content']) # markdown is use to display content of message, that will be displayed inside box
        # we use this format message['content'] because the message is in form of dictionary{key:value} as role,content
        #- and to retrieve some thing out of dictionary we use square brackets like dictionary[key] or dictionary[value]
        # message in for loop is a temporary variable in which the data inside the chathistory will be stored, and that data is actually a dictionary as key value pair
    # this message is a temporary variable,message contains role and content

with st.sidebar:
    st.header("⚙️ Settings")

    temperature = st.slider("Adjust temperature for creative responses", 0.0, 1.0, 0.0, 0.1)

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# llm inititiate
llm= ChatGroq(
    model='llama-3.1-8b-instant',
    temperature=temperature
)
# input box where user can type some thing
user_prompt= st.chat_input('Ask ChatBot') # to get a box interface  where u enter query
if user_prompt: # condition if user gives prompt
    with st.chat_message('user'): # will create `box for user's message
      st.markdown(user_prompt) # will display user's message on the screen in the box
    # appending/saving the user's message in chat_history
    st.session_state.chat_history.append({'role':'user','content':user_prompt})
    # sending chat history to llm
    response=llm.invoke(
         input= [{'role':'system','content':'you are a helpful assistant'} , *st.session_state.chat_history]
    )# * operator is to unpack items in list,passing a list because list contain multiple messages as key value pair,
    assistant_response= response.content
    st.session_state.chat_history.append({'role': 'assistant','content': assistant_response})
    with st.chat_message('assistant'):
        st.markdown(assistant_response)