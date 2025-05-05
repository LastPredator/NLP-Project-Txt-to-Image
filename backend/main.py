import grpc
from concurrent import futures
import time
import image_gen_pb2
import image_gen_pb2_grpc
from model_loader import load_model
from generate import generate_image
from generate_video import generate_video_from_image



class ImageGenServicer(image_gen_pb2_grpc.ImageGeneratorServicer):
    def __init__(self):
        self.model = load_model()

    def GenerateImage(self, request, context):
        prompt = request.text + " " + request.context
        try:
            img_b64 = generate_image(
                self.model,
                prompt,
                width=request.width or 512,
                height=request.height or 512
            )
            return image_gen_pb2.ImageResponse(image=img_b64, status="success")
        except Exception as e:
            return image_gen_pb2.ImageResponse(image="", status=f"error: {str(e)}")

    def GenerateVideo(self, request, context):
        try:
            video_b64 = generate_video_from_image(request.image)
            return image_gen_pb2.VideoResponse(video=video_b64, status="success")
        except Exception as e:
            return image_gen_pb2.VideoResponse(video="", status=f"error: {str(e)}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    image_gen_pb2_grpc.add_ImageGeneratorServicer_to_server(ImageGenServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
