import random
import pprint
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)
import pytest


def getRandLetter():
    return chr(random.randint(ord("a"), ord("z")))


def getRandWord():
    wlen = 10
    wlst = [getRandLetter() for _ in range(wlen)]
    word = "".join(wlst)
    return word


def dec(curWrd):
    diffList = []
    prm = {"msg": curWrd}
    rsp = client.post("/encrypt", json={"msg": curWrd}).json()
    encrypted = rsp["encrypted"]
    diffList.append(len(encrypted) / len(curWrd))
    prm = {"dec": encrypted, "destroy": "True"}
    rbp = client.post("/decrypt", json=prm).json()
    pprint.pprint(rbp)
    decrypted = rbp["msg"]
    return decrypted


def test_answer():
    curWrd = getRandWord()
    assert dec(curWrd) == curWrd
