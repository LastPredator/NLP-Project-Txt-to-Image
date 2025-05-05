import grpc
import base64
import image_gen_pb2
import image_gen_pb2_grpc

def get_image(prompt, context, width=512, height=512):
    channel = grpc.insecure_channel("localhost:50051")
    stub = image_gen_pb2_grpc.ImageGeneratorStub(channel)

    req = image_gen_pb2.TextRequest(
        text=prompt,
        context=context,
        width=width,
        height=height
    )

    res = stub.GenerateImage(req)

    if res.status == "success":
        return base64.b64decode(res.image), None
    return None, res.status

def get_video_from_image(base64_image):
    channel = grpc.insecure_channel("localhost:50051")
    stub = image_gen_pb2_grpc.ImageGeneratorStub(channel)

    req = image_gen_pb2.VideoRequest(image=base64_image)
    res = stub.GenerateVideo(req)

    if res.status == "success":
        return base64.b64decode(res.video), None
    return None, res.status

