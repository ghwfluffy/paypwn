from fastapi import FastAPI, Depends
from google.protobuf.json_format import MessageToDict, ParseDict

from sqlalchemy import create_engine

from api.Status_pb2 import StatusRequest, StatusResponse

from pbdantic.api.Status_p2p import StatusRequest as StatusRequestModel
from pbdantic.api.Status_p2p import StatusResponse as StatusResponseModel

from db.user import User

app = FastAPI()

@app.get("/status", response_model=StatusResponseModel)
async def get_status(params: StatusRequestModel = Depends()):
    request = ParseDict(params.dict(), StatusRequest())

    response = StatusResponse()
    response.context = request.context
    response.version = "0.1"

    return MessageToDict(response)

if __name__ == "__main__":
    DATABASE_URL = "postgresql+psycopg2://paypwn:paypwn@postgres/paypwn"

    engine = create_engine(DATABASE_URL)
    User.create(engine)

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
