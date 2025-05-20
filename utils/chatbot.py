from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

def get_chatbot_response(message: str) -> str:
    medical_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
    You are Ema, an advanced AI medical assistant.
    Your goal is to provide clear, factual, and concise answers to medical queries.
    Always maintain a professional yet friendly tone.

    Guidelines:
    - If unsure, acknowledge uncertainty and recommend consulting a healthcare provider
    - Focus on general medical information and avoid specific diagnoses
    - Provide sources when discussing medical facts
    - Break down complex medical terms
    - Use bullet points for lists
    - Format important information in **bold**

    User Query: {query}

    Response:
    """
    )

    llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-04-17",
    temperature=0.2,
    convert_system_message_to_human=True,
    google_api_key=api_key
    )

    chain = LLMChain(llm=llm, prompt=medical_prompt)
    return chain.run(query=message)



