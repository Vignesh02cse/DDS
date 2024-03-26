import base64

import streamlit as st
from openai import RateLimitError
from streamlit_chat import message

from backend.core import run_llm, calculate_depression_percentage


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
