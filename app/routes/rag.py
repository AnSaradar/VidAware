from fastapi import FastAPI, APIRouter, Depends, UploadFile, status ,Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings ,Settings
import logging
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai


data_router = APIRouter(
    prefix="/rag",
    tags=["rag"],
)

logger = logging.getLogger('uvivorn.error')

app_settings = get_settings()

def load_text_file(path):
    with open(path, 'r') as file:
        transcription = file.read()

    return transcription

def chunking(transcription):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(transcription)
    return chunks

def calculate_embeddings(chunks):
    embeddings_model = OpenAIEmbeddings(openai_api_key=app_settings.OPENAI_API_KEY)
    embeddings = [embeddings_model.embed(chunk) for chunk in chunks]
    vector_store = FAISS.from_embeddings(embeddings, chunks)
    vector_store.save("vector_store.faiss")

    return embeddings , vector_store



@data_router.post("/process")
async def process(file:UploadFile):
    try:
        text = await file.read()
        text = text.decode('utf-8')
        chunks = chunking(text)

        embeddings , vector_store = calculate_embeddings(chunks)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "embeddings": embeddings
            }
        )
    except Exception as e:
        logger.error(f"Error while processing file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Error while processing file"
            }
        )




