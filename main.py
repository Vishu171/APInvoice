import streamlit as st
import altair as alt
import prompts
from PIL import Image
from io import StringIO
import pandas as pd

# Page Icon
hyattimage = Image.open("assets/jadeglobal.png")
st.set_page_config(page_title="Jade Global",page_icon=hyattimage,layout="wide")

# Credentials to login into app
username=st.secrets["streamlit_username"]
password=st.secrets["streamlit_password"]

# adding this to test out caching
st.cache_data(ttl=86400)

#Functions used

# Function for chat history
def chat_history(CSV_FILE):
    try:
        chat_history_df = pd.read_csv(CSV_FILE)
        return chat_history_df
    except FileNotFoundError:
        chat_history_df = pd.DataFrame(columns=["User_Chat_History"])
        chat_history_df.to_csv(CSV_FILE, index=False)
        return chat_history_df

# Function for Login authentication
def creds_entered():
    if len(st.session_state["streamlit_username"])>0 and len(st.session_state["streamlit_password"])>0:
          if  st.session_state["streamlit_username"].strip() != username or st.session_state["streamlit_password"].strip() != password: 
              st.session_state["authenticated"] = False
              st.error("Invalid Username/Password ")

          elif st.session_state["streamlit_username"].strip() == username and st.session_state["streamlit_password"].strip() == password:
              st.session_state["authenticated"] = True

def authenticate_user():
      if "authenticated" not in st.session_state:
        buff, col, buff2 = st.columns([1,1,1])
        col.text_input(label="Username:", value="", key="streamlit_username", on_change=creds_entered) 
        col.text_input(label="Password", value="", key="streamlit_password", type="password", on_change=creds_entered)
        return False
      else:
           if st.session_state["authenticated"]: 
                return True
           else:  
                  buff, col, buff2 = st.columns([1,1,1])
                  col.text_input(label="Username:", value="", key="streamlit_username", on_change=creds_entered) 
                  col.text_input(label="Password:", value="", key="streamlit_password", type="password", on_change=creds_entered)
                  return False

# if the user is authenticated
if authenticate_user():
   his_file = "Chat_History/jade_Chat_History.csv"
   chat_df = chat_history(his_file)
   st.markdown(
    """
       <style>
           [data-testid=stSidebar] [data-testid=stImage]{
               text-align: center;
               display: block;
               margin-left: auto;
               margin-right: auto;
               width: 100%;
           }
       </style>
       """, unsafe_allow_html=True
       )
   with st.sidebar:
            image = Image.open("assets/jadeglobal.png")
            image = st.image('assets/jadeglobal.png',width=290)
            st.write("""
            ## Solution for L1 and L2 team 
            """)
            st.write("""

            """)
            st.write("""

            """)

   # Enter a question in chat box
   query = st.chat_input("Enter your question:")
   st.markdown(""" ##### AI assisted solution to extract information from SOPs:

    
    ##### Post your queries in the textbox at bottom of this page. 
   """)
   
   # Create a text input to edit the selected question
   if "messages_1" not in st.session_state.keys():
       st.session_state.messages_1 = []
   
   new_data = {"User_Chat_History" : query}
   chat_df = chat_df._append(new_data, ignore_index=True)
   chat_df = chat_df.dropna().sort_index(axis=0, ascending=False)
   chat_df = chat_df.sort_index(axis=0, ascending=False)
   #st.sidebar.dataframe(chat_df,hide_index=True, use_container_width=True)
   chat_df.to_csv(his_file, index=False)
   chat_reset = st.sidebar.button(":orange[Clear Chat History]", type="secondary", key="Clear_Chat_History")
   if chat_reset:
     chat_df = pd.DataFrame(columns=["User_Chat_History"])
     chat_df.to_csv(his_file, index=False)
   
   for message in st.session_state.messages_1:
     with st.chat_message(message["role"]):
         st.markdown(message["content"], unsafe_allow_html = True)
   
   with st.sidebar:
     for index, row in chat_df.iterrows():
         if st.button(f"{row['User_Chat_History']}",key=f"button_{index}"):
             query = str(row['User_Chat_History'])
   
   if prompt1 := query:
     st.chat_message("user").markdown(prompt1, unsafe_allow_html = True)
       # Add user message to chat history
     st.session_state.messages_1.append({"role": "user", "content": prompt1})
     try:
         with st.chat_message("assistant"):
           result = prompts.letter_chain(query)
           answer = result['result']
           st.markdown(answer)
           st.session_state.messages_1.append({"role": "assistant", "content":answer } )
     except Exception as error:
                     st.write(error)
                     st.write("Please try to improve your question.")
