import uvicorn
import os
import logging
from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette.responses import JSONResponse

from llms.translate_v1 import translate_v1
from llms.polish_v1 import polish_v1

log_path = os.path.join(os.path.dirname(__file__), 'serve.log')
logging.basicConfig(
    filename=log_path,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

app = FastAPI()


class TranslationInput(BaseModel):
    text: str
    target_language: str


class PolishInput(BaseModel):
    text: str


class TranslateOutput(BaseModel):
    processed_text: str


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"服务器内部错误: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误，请联系管理员。"},
    )


@app.post("/translate", response_model=TranslateOutput)
async def translate(request: TranslationInput) -> TranslateOutput:
    translation = translate_v1(text=request.text, target_language=request.target_language)
    return TranslateOutput(processed_text=translation)


@app.post("/polish", response_model=TranslateOutput)
async def polish(request: PolishInput) -> TranslateOutput:
    translation = polish_v1(text=request.text)
    return TranslateOutput(processed_text=translation)


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True, log_level="debug")
