from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from encryptMessage import Encryptor
from pydantic import BaseModel

app = FastAPI(title="The encryptii api")
enc = Encryptor()
origins = [
    "http://127.0.0.1",
    "http://localhost:3000",
    "https://encryptii.vercel.app",
    "https://encryptii-server.herokuapp.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class encryptINP(BaseModel):
    msg: str
    auto_destroy: bool = False
    emoji: bool = False


class decryptINP(BaseModel):
    dec: str
    destroy: bool = True


@app.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def routePage():
    response = RedirectResponse(url="/docs")
    return response


@app.get("/ping")
def pingpong():
    return {"ping": "pong"}


@app.post("/encrypt", status_code=status.HTTP_201_CREATED)
async def encryption(pmt: encryptINP):
    msg = pmt.msg
    encrypted = enc.encrypt(msg, pmt.emoji)
    resp = {"encrypted": encrypted}
    return resp


@app.get("/encrypt", status_code=status.HTTP_201_CREATED)
async def getEncryption(msg: str):
    encrypted = enc.encrypt(msg)
    resp = {"encrypted": encrypted}
    return resp


@app.post("/decrypt", status_code=status.HTTP_200_OK)
async def decryption(pmt: decryptINP, response: Response):
    dec = pmt.dec.encode()
    des = pmt.destroy
    d = enc.decrypt(dec, des)
    if d == -1:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "Message does not exist or was destroyed"}
    else:
        return {"msg": str(d)}


@app.get("/decrypt", status_code=status.HTTP_200_OK)
async def getDecryption(dec: str, response: Response, des: bool = True):
    dec = dec.encode()
    d = enc.decrypt(dec, des)
    if d == -1:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "Message does not exist or was destroyed"}
    else:
        return {"msg": str(d)}
