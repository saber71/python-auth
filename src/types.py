from typing import Union

from pydantic import BaseModel


class Base(BaseModel):
    id: str
    storageType: Union[str, None]

class Auth(Base):
    id: str
    password: str
    storageType: Union[str, None]
