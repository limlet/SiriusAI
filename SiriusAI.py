from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import whisper
import requests
app=FastAPI()

# Инициализация моделей
sum=pipeline("summarization", model="facebook/bart-large-cnn")
spm=whisper.load_model("base")
class yaclient:
    def __init__(self,token):
        self.token=token
        self.base_url="https://cloud-api.yandex.net/v1/disk"
    def get_headers(self):
        return {
            "Authorization": f"OAuth {self.token}"
        }
    def dwf(self, file_path):
        dld_url=f"{self.base_url}/resources/download?path={file_path}"
        res=requests.get(dld_url, headers=self.get_headers())
        res.raise_for_status()
        dwl=res.json().get("href")
        video_response=requests.get(dwl)
        with open("video.mp4", "wb") as f:
            f.write(video_response.content)
# Функция для транскрипции видео
def tv(video_path):
    result=spm.transcribe(video_path)
    return result['text']
# Функция для суммаризации текста
def st(text):
    summary=sum(text,max_length=130,min_length=30,do_sample=False)
    return summary[0]['summary_text']

class VR(BaseModel):
    file_path: str

@app.post("/summarize_video")
async def summarize_video(request:VR):
    try:
        # Шаг 1: Скачиваем видео с Яндекс.Диска
        yc.dwf(request.file_path)
        # Шаг 2: Преобразуем видео в текст
        text=tv('video.mp4')
        # Шаг 3: Суммаризируем текст
        s=st(text)
        return {"summary": s}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Инициализация клиента Яндекс.Диска с токеном
token="ваш_oauth_токен"
yc=yaclient(token)
