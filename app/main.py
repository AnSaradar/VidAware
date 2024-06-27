from fastapi import FastAPI ,status ,HTTPException
from fastapi.responses import JSONResponse
from core import YoutubeHandler
from routes import base , rag , llm

app = FastAPI()

app.include_router(base.base_router)
app.include_router(rag.data_router)
app.include_router(llm.llm_router)
def main():
    text_file , text_language = YoutubeHandler().convert_video_to_text("https://www.youtube.com/watch?v=qppV3n3YlF8&t=1s")
    print(text_file , text_language)


if __name__ == "__main__":
    main()