import streamlit as st
import openai
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS, Pinecone
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
# import pinecone



LETTER_TEMPLATE = """ Your Objective is to Extract and display detailed information from invoices that you will get as \context.

Details Required:

For an example:

{
    "invoice_number": "INV-12345",
    "invoice_date": "2024-07-01",
    "customer": {
        "name": "John Doe",
        "address": "123 Elm Street, Springfield, IL"
    },
    "items": [
        {
            "description": "Item A",
            "quantity": 2,
            "unit_price": 50.00
        },
        {
            "description": "Item B",
            "quantity": 3,
            "unit_price": 30.00
        }
    ],
    "total_amount": 190.00,
    "due_date": "2024-07-15",
    "payment_status": "Paid",
    "currency": "USD",
    "created_by": "Admin",
    "last_modified_date": "2024-07-05"
}

Context: ```{context}```

Question: ```{question}```

Your invoices details are:
"""
LETTER_PROMPT = PromptTemplate(input_variables=["question", "context"], template=LETTER_TEMPLATE, )

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.1,
    max_tokens=1000, 
    openai_api_key=st.secrets["openai_key"]
)


def get_faiss():
    " get the loaded FAISS embeddings"
    embeddings = OpenAIEmbeddings(model = "text-embedding-3-small",openai_api_key=st.secrets["openai_key"])
    return FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization = True)


def letter_chain(question):
    """returns a question answer chain for pinecone vectordb"""
    
    docsearch = get_faiss()
    retreiver = docsearch.as_retriever(#
        #search_type="similarity", #"similarity", "mmr"
        search_kwargs={"k":3}
    )
    qa_chain = RetrievalQA.from_chain_type(llm, 
                                            retriever=retreiver,
                                           chain_type="stuff", #"stuff", "map_reduce","refine", "map_rerank"
                                           return_source_documents=True,
                                           chain_type_kwargs={"prompt": LETTER_PROMPT}
                                          )
    return qa_chain({"query": question})
