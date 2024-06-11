from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel, create_model, Field
from typing import Type, List, Dict, Any
from google.protobuf.json_format import MessageToDict, ParseDict

from Status_pb2 import StatusRequest, StatusResponse

def protobuf_to_pydantic(protobuf_class: Type[Any]) -> Type[BaseModel]:
    def get_field_type(field):
        if field.type == field.TYPE_BOOL:
            return bool
        elif field.type == field.TYPE_STRING:
            return str
        elif field.type == field.TYPE_INT32:
            return int
        elif field.type == field.TYPE_MESSAGE:
            nested_model = protobuf_to_pydantic(field.message_type._concrete_class)
            return nested_model
        else:
            raise TypeError(f"Unsupported field type: {field.type}")

    fields = {}
    for field in protobuf_class.DESCRIPTOR.fields:
        field_type = get_field_type(field)
        default_value = Query(False) if field_type == bool else Query("") if field_type == str else Query(0)
        fields[field.name] = (field_type, default_value)

    return create_model(protobuf_class.__name__, **fields)

StatusRequestModel = protobuf_to_pydantic(StatusRequest)

app = FastAPI()
@app.get("/status")
async def get_status(params: StatusRequestModel = Depends()):
    request = ParseDict(params.dict(), StatusRequest())

    response = StatusResponse()
    response.context = request.context
    response.version = "0.1"

    return MessageToDict(response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
