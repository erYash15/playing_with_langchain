import uvicorn
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")
## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="groqapi"

model = ChatGroq(model='gemma2-9b-it', groq_api_key=groq_api_key)
parser = StrOutputParser()

generic_template="Translate the following into {language}:"
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", generic_template),
        ("user", "{text}")
    ]
)

# create chain
chain = prompt|model|parser

# App Defination
app=FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API server using langchain runnable interfaces"
)

add_routes(
    app, chain, path="/chain"
)

if __name__ == "__main__":
    uvicorn.run(app,host="localhost", port=8000)