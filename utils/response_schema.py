from pydantic import BaseModel, ConfigDict

class ResponseBase(BaseModel):
    def to_response_dict(self):
        return self.model_dump(mode="json")


class OrmBase(ResponseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class GenericResponse(BaseModel):
    msg: str
