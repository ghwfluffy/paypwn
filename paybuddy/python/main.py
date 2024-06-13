from fastapi import FastAPI, Depends
from google.protobuf.json_format import MessageToDict, ParseDict

from Status_pb2 import StatusRequest, StatusResponse

from pbdantic.Status_p2p import StatusRequest as StatusRequestModel
from pbdantic.Status_p2p import StatusResponse as StatusResponseModel

app = FastAPI()

@app.get("/status", response_model=StatusResponseModel)
async def get_status(params: StatusRequestModel = Depends()):
    request = ParseDict(params.dict(), StatusRequest())

    response = StatusResponse()
    response.context = request.context
    response.version = "0.1"

    return MessageToDict(response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
