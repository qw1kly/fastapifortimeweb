from typing import Any
from fastapi import FastAPI, Request, Body, WebSocket, WebSocketDisconnect, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import asyncio
from models import make_address_payment,get_bal_wal,trans_history, gift_for_riddle, auth_check_password,register_password, auth_password,rat_win, auth,get_friends, game_ch,get_profile, referation_system, register, register_name, one_win, get_nickname
import aiofiles
from urllib.parse import unquote
from auth import check_pass
from aiogram.methods.create_invoice_link import CreateInvoiceLink
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot
from aiogram import types
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import aiomysql

app = FastAPI()
templates = Jinja2Templates(directory='templates')

app.add_middleware(
   CORSMiddleware,
   allow_origins=['https://qw1kly-reactfortimeweb-d700.twc1.net',],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)
                  
@app.get('/')
async def index(request: Request):
    return {'aaa':1}

@app.post('/')
async def index(payload: Any = Body(None)):
   
    idi = str(payload['telegramidi'])
    pasw = payload['password']
    boolean_f = asyncio.create_task(auth_check_password([idi, pasw]))
    return await boolean_f


@app.get('/game')
async def index(request: Request):
    return {'aaa':1}


@app.post('/game')
async def update_item(payload: Any = Body(None)):
    m = payload
    try:
        idi = m['telegram']
    except:
        idi = m['telegramid']
    boolean = await asyncio.create_task(check_pass([idi, m['password']]))
    if boolean:
        if m.get("telegramid"):
            game_db = asyncio.create_task(game_ch([m["password"], idi]))
            return await game_db
        elif m.get("telegram"):
            auth_db = asyncio.create_task(auth([m["password"], idi]))
            return await auth_db
        elif m.get("register"):
            check_auth = asyncio.create_task(register([m["password"], idi]))
            return await check_auth
    return False


@app.get('/rating')
async def indexx(request: Request):
    return templates.TemplateResponse(name="game.html", request=request)


@app.post('/rating') # RETURNING KEY:DATA, WHERE DATA1 = BALANCE, DATA2 = ACCESS TO CHAT(TOP 5)
async def indexxx(payload: Any = Body(None)):
    m = payload

  
    if m.get("winners"):
        sel_win = asyncio.create_task(rat_win(m))
        return await sel_win
    elif m.get('selectwinner'):
        one_win_ = asyncio.create_task(one_win([123, m['selectwinner']]))
        return await one_win_
    elif m.get("actname"):
        get_nick = asyncio.create_task(get_nickname([123, m['actname']]))
        return await get_nick
    elif m.get("telegramidi"):
        idi = m['telegramidi']
        get_auth = asyncio.create_task(auth_password([idi, m['password']]))
        return await get_auth

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/rating")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            await manager.broadcast(f"{data}<br />")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/ref/{user_id}")
async def ref_system(user_id, request: Request):
    return templates.TemplateResponse(name="testing_ref.html", request=request)


@app.post("/ref")
async def ref_system_post(payload: Any = Body(None)):
    m = list(map(lambda x: x.split('='), payload.decode('utf-8').split('&')))
    ref_s = asyncio.create_task(referation_system(m))
    return await ref_s


@app.get("/register")
async def register_user(request: Request):
    return templates.TemplateResponse(name='register.html', request=request)




@app.post("/register2")
async def ref_system_post(payload: Any = Body(None)):
    m = payload
    if m.get("name"):
        
        json = {'nickname':m['name'], 'id':m['telegramtodelete']}
        name_todb = asyncio.create_task(register_name(json))
        return await name_todb
    elif m.get('password'):
        
        json = {'password': m['password'], 'id': m["telegramtodelete"]}
        pass_todb = asyncio.create_task(register_password(json))
        return await pass_todb

@app.get("/store")
async def ref_system_post(request: Request):
    return templates.TemplateResponse(name="store.html", request=request)

@app.post("/store")
async def ref_system_post(payload: Any = Body(None)):
    m = payload.decode('utf-8').split('=')
    m[-1] = unquote(m[-1])
    if len(m)==2 and m[0] == 'telegramidi':
        return await asyncio.create_task(get_bal_wal(m))
    elif len(m)==3 and m[0] == 'telegramidi':
        m[1]=m[1].split("&adrr")[0]
        m = [m[1], m[2]]
        return await asyncio.create_task(make_address_payment(m))


@app.get("/profile")
async def profile(request: Request):
    return templates.TemplateResponse(name="profile.html", request=request)



@app.post("/profile")
async def ref_system_post(payload: Any = Body(None)):
    m = payload
    if m.get("friends"):
        profile_data = asyncio.create_task(get_friends([123, m['friends']]))
    
        return await profile_data
    elif m.get("profilename"):
        profile_data = asyncio.create_task(get_profile([123, m['profilename']]))
        print(await profile_data)
        return await profile_data

@app.post("/riddle")
async def riddle(payload: Any = Body(None)):
    m = payload
    if m['riddle'] == 'India':
        m = [m['telegram'], m['riddle']]
        return await asyncio.create_task(gift_for_riddle(m))
    return {1:3}
