from openai import OpenAI
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title(" 🤖 Intelligent OFET Assistant")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

st.image('Fig1.jpg', caption='Intelligent OFET Assistant')
st.markdown(
"""
## Introduction

The framework of the method proposed in this study is divided into three main modules: 

(a) a data preprocessing toolbox, (b) human-in-the-loop prompt engineering, and (c) in-depth data analysis of the constructed tabular dataset. 

During the data preprocessing stage, the toolbox plays a pivotal role by dissecting PDF format academic literature into textual content, tabular data, and image data using pre-written Python code and the GPT-4V model. 

It is important to note that numerous OFET device diagrams incorporate crucial fabrication parameters. These include the geometric configuration of the device, the denomination of source and drain electrodes, along with the material of the dielectric layer. Therefore, this study primarily emphasizes the image data content of OFET device structures. Furthermore, to facilitate subsequent analysis of semiconductor materials' molecular characteristics using cheminformatics tools, we employed the DECIMER tool to effortlessly convert molecular images of semiconductor materials in the literature into SMILES format text. Lastly, to mitigate potential hallucination from the large model and enhance the accuracy of text mining, we embedded common chemical knowledge into the prompts, such as restricting the extraction of OFET geometric structures to only one of four types: BGBC, BGTC, TGBC, or TGTC.
"""
)


# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input():
#     if not openai_api_key:
#         st.info("Please add your OpenAI API key to continue.")
#         st.stop()

#     client = OpenAI(api_key=openai_api_key)
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)
#     response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
#     msg = response.choices[0].message.content
#     st.session_state.messages.append({"role": "assistant", "content": msg})
#     st.chat_message("assistant").write(msg)
