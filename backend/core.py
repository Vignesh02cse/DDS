import os
from typing import Any, Dict, List

from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Pinecone
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
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
