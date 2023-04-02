from fastapi import APIRouter
import pykakasi
import api.schemas.rhyme as rhyme_schema

kks = pykakasi.kakasi()

router = APIRouter()

@router.post("/judge", response_model=rhyme_schema.RhymeScore)
async def judge_rhyme(request_body: rhyme_schema.RhymeInput):
    title = kks.convert(request_body.title)
    print(''.join([item["hepburn"] for item in title]))
    input = kks.convert(request_body.input)
    print(''.join([item["hepburn"] for item in input]))
    return rhyme_schema.RhymeScore(score=8, title="断頭台", input="パッとしない")