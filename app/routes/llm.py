from fastapi import FastAPI, APIRouter, Depends, UploadFile, status ,Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings ,Settings
from langchain_openai.chat_models import ChatOpenAI
from models import QuestionRequest
from langchain_core.output_parsers import StrOutputParser

llm_router = APIRouter(
    prefix="/llm",
    tags=["llm"],
)
app_settings = get_settings()

model = ChatOpenAI(openai_api_key=app_settings.OPENAI_API_KEY, model="gpt-3.5-turbo")
parser = StrOutputParser()

pipeline = model | parser



@llm_router.post("/invoke")
async def send(request: QuestionRequest):
    try:
        response = pipeline.invoke(request.question)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": response
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": str(e)
            }
        )



