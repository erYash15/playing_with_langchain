import os
from dotenv import load_dotenv

from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="GENAIAPPWithOllama"
## Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the question asked."),
        ("user", "Question:{question}")
    ]
)

st.title("Langchain Demo with Gemma3:b1")
input_text = st.text_input("What question you have in mind?")

llm=Ollama(model="gemma3:1b")
output_parser = StrOutputParser()
chain = prompt|llm|output_parser


if input_text:
    output = chain.invoke({"question":input_text})
    st.write(output)