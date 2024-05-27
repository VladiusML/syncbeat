from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from syncbeats.likes.dao import LikeDAO
from fastapi_cache.decorator import cache

router = APIRouter()
templates = Jinja2Templates(directory="syncbeats/templates")

clients = []

@router.get("/total-likes")
@cache(expire=60)
async def get_total_likes():
    total_likes = await LikeDAO.get_total_likes()
    return {"total_likes": total_likes}

@router.websocket("/ws/like")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "like":
                await LikeDAO.increment(user_id)  # Передача user_id в метод increment
                count = await LikeDAO.get_total_likes()  # Учитывайте user_id при получении количества лайков
                for client in clients:
                    await client.send_text(str(count))
    except WebSocketDisconnect:
        clients.remove(websocket)