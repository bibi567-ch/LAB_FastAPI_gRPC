from concurrent import futures
import random
import time

import grpc

import protobufs.crypto_pb2 as crypto_pb2
import protobufs.crypto_pb2_grpc as crypto_pb2_grpc


class CryptoMarketService(crypto_pb2_grpc.CryptoServiceServicer):
    def __init__(self):
        self.base_prices = {
            "bitcoin": 65000.0,
            "ethereum": 3500.0,
            "solana": 150.0,
            "dogecoin": 0.15,
        }

    def StreamMarketData(self, request, context):
        ticker = request.ticker.lower()
        if not ticker:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "El ticker no puede estar vacío.")

        current_price = self.base_prices.get(ticker, 100.0)
        interval = max(1, request.interval_seconds)

        for _ in range(12):
            current_price *= random.uniform(0.985, 1.015)
            yield crypto_pb2.MarketDataResponse(
                ticker=ticker,
                price_usd=round(current_price, 2),
                timestamp=int(time.time()),
            )
            time.sleep(interval)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    crypto_pb2_grpc.add_CryptoServiceServicer_to_server(CryptoMarketService(), server)
    port = "50051"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Servidor gRPC de criptomonedas activo en el puerto {port}...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
