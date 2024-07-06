import uvicorn

from fastapi import FastAPI, Depends
from google.protobuf.json_format import MessageToDict, ParseDict

from sqlalchemy import Engine

from paybuddy_pb.api.Status_pb2 import StatusRequest, StatusResponse
from paybuddy_pb.api.Status_p2p import StatusRequest as StatusRequestModel
from paybuddy_pb.api.Status_p2p import StatusResponse as StatusResponseModel

from paypwn.db.connect import connect_db

from paypwn.db.user import User
from paybuddy.db.account_balance import AccountBalance
from paybuddy.db.linked_account import LinkedAccount
from paybuddy.db.transfer import Transfer

VERSION = "0.1"

app = FastAPI(
    root_path="/paybuddy/api",
    title="PayBuddy API",
    description="API documentation for PayBuddy service.",
    version=VERSION,
)

@app.get("/status", response_model=StatusResponseModel)
async def get_status(params: StatusRequestModel = Depends()):
    request = ParseDict(params.dict(), StatusRequest())

    response = StatusResponse()
    response.context = request.context
    response.version = VERSION

    return MessageToDict(response)

if __name__ == "__main__":

    engine: Engine = connect_db()
    User.create(engine)
    AccountBalance.create(engine)
    LinkedAccount.create(engine)
    Transfer.create(engine)

    uvicorn.run(app, host="0.0.0.0", port=8080)
