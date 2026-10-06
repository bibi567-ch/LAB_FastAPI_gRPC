import asyncio

import grpc
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import protobufs.crypto_pb2 as crypto_pb2
import protobufs.crypto_pb2_grpc as crypto_pb2_grpc

app = FastAPI(title="Gateway gRPC + WebSocket")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def get_index():
    with open("static/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())


@app.websocket("/ws/crypto/{ticker}")
async def websocket_crypto_endpoint(websocket: WebSocket, ticker: str):
    await websocket.accept()

    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = crypto_pb2_grpc.CryptoServiceStub(channel)
        request = crypto_pb2.StreamRequest(ticker=ticker, interval_seconds=3)

        try:
            async for response in stub.StreamMarketData(request):
                payload = {
                    "ticker": response.ticker,
                    "price": response.price_usd,
                    "timestamp": response.timestamp,
                }
                await websocket.send_json(payload)
        except (WebSocketDisconnect, Exception):
            pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("web_app:app", host="127.0.0.1", port=8001, reload=True)
