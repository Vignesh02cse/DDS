import base64
import os
from typing import Any, Dict, List

import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Pinecone
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from openai import RateLimitError
from streamlit_chat import message
from transformers import pipeline

# import pinecone
#
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
# PINECONE_ENVIRONMENT_REGION = os.environ.get("PINECONE_ENVIRONMENT_REGION")
#
# pinecone.init(
#     api_key=os.environ["PINECONE_API_KEY"],
#     environment=os.environ["PINECONE_ENVIRONMENT_REGION"])
#
# INDEX_NAME = "mental"


# Initialize the sentiment analysis pipeline
nlp = pipeline("sentiment-analysis")


def calculate_depression_percentage(texts):
    # Initialize a counter for depressive texts
    depressive_text_count = 0
    # Analyze each text
    for text in texts:
        result = nlp(text)
        # If the sentiment is negative, increment the counter
        if result[0]['label'] == 'NEGATIVE':
            depressive_text_count += 1

    # Calculate and return the depression percentage
    depression_percentage = round(((depressive_text_count / len(texts)) * 100), 2)
    return depression_percentage


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    # '''retrive the data from vectorstore and generate the response'''
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    docsearch = Pinecone.from_existing_index(
        embedding=embeddings,
        index_name='mental',
    )

    # """Run the LLM model with the given query and chat history."""
    chat = ChatOpenAI(
        verbose=True,
        temperature=0.5,
        max_tokens=100,
    )
    # """sementic search and generate the response"""
    qa = ConversationalRetrievalChain.from_llm(
        llm=chat, retriever=docsearch.as_retriever(), return_source_documents=True
    )
    return qa({"question": query, "chat_history": chat_history})

def clear_text():
    st.session_state.prompt = ""


st.set_page_config(
    page_title="MHT ChatBot", page_icon='static/Doc.jpg'
)

LOGO_IMAGE = "static/DoctorAnime.png"

st.markdown(
    """
    <style>
    .container {
        display: flex;
        background-color: #5eabff;
        border: 10px solid 	#5eabff;
        border-radius: 50px;
        padding: 10px;
        top: 0;
        
    }
    .logo-text {
        font-weight:1000 !important;
        font-size:50px !important;
        color: #000000 !important;  # Change the color here
        padding-top: 10px !important;
    }
    .logo-img {
        float:right;
        width: 80px;
        height: 80px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}"><br>
        <p class="logo-text">Mental-health ChatBot &#129302;</p>
    </div>
    """,
    unsafe_allow_html=True
)

if (
        "chat_answers_history" not in st.session_state
        and "user_prompt_history" not in st.session_state
        and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

prompt = st.text_input("Prompt", placeholder="Ask anything...") or st.button("Submit")

end_session = st.button("End Session")

if prompt:
    with st.spinner("Generating response..."):
        try:
            generated_response = run_llm(query=prompt, chat_history=st.session_state["chat_history"])
            formatted_response = (f"{generated_response['answer']}")

            st.session_state.chat_history.append((prompt, generated_response["answer"]))
            st.session_state.user_prompt_history.append(prompt)

            st.session_state.chat_answers_history.append(formatted_response)

            clear_text()
        except RateLimitError:
            print("Retry in 20 seconds")
            st.error('Retry in 20 seconds', icon="🚨")

if end_session:
    depression_percentage = calculate_depression_percentage(st.session_state["user_prompt_history"])
    st.write(f"Depression Percentage: {depression_percentage}%")

    with open('chat_history.txt', 'w') as f:
        for user_query, generated_response in zip(st.session_state["user_prompt_history"],
                                                  st.session_state["chat_answers_history"]):
            f.write(f"User: {user_query}\n")
            f.write(f"Bot: {generated_response}\n")

if st.session_state["chat_answers_history"]:
    for i, (generated_response, user_query) in enumerate(zip(
            reversed(st.session_state["chat_answers_history"]),
            reversed(st.session_state["user_prompt_history"]),
    )):
        message(
            user_query,
            is_user=True,
            key=f"user_query_{i}",
        )
        message(generated_response, key=f"generated_response_{i}")
