from typing import List

from fastapi import FastAPI, Form
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from settings import settings
import aiohttp
from pydantic import BaseModel

app = FastAPI(
    title="AIChatAPI",
    description="AIChatAPI is a simple API that uses OpenAI's GPT-3 API to generate responses to messages.",
    version="0.1.0",
)
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
)
app.mount('/assets', StaticFiles(directory='assets'), name='assets')


class MessageBody(BaseModel):
    msg: str
    history: List[List[str]] = []
    prompt: str = ''
    token: str = None


index_html = open('templates/index.html', 'r', encoding='utf-8').read()


@app.get("/")
async def root():
    return HTMLResponse(index_html)


@app.put('/', description='密码通过看启动日志获取，每次重启都会变')
async def put_root(pwd: str, token: str):
    if pwd != settings.PASSWORD:
        return {'code': 403, 'msg': 'wrong password'}
    settings.API_KEY = token
    return {'code': 200, 'msg': 'ok'}


@app.post("/")
async def root(message: MessageBody):
    for i in message.history:
        message.prompt += f'Question:\n{i[0]}\nAI:\n{i[1]}\n'
    message.prompt += f'Question:\n{message.msg}\nAI:\n'
    data = {
        "model": "text-davinci-003",
        "prompt": message.prompt,
        "max_tokens": 1000 if message.token else settings.FREE_TOKENS,
        "temperature": 0.9,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": [
            "\nAI:",
            "\nQuestion:",
        ]
    }
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.post('https://api.openai.com/v1/completions', headers=settings.headers(message.token),
                                json=data) as resp:
            res = await resp.json()
            if res.get('error'):
                return {'code': 500, 'msg': 'error', 'data': 'API_KEY无效或者过期'}
            else:
                data = res['choices'][0]['text']
                msg = '回复过长，已被截断，如需更长的回复，请购买API_KEY' \
                    if res['usage']['completion_tokens'] == settings.FREE_TOKENS else 'success'
                return {'code': 200, 'msg': msg, 'data': [message.msg, data]}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=False, workers=1)
