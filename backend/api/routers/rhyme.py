from fastapi import APIRouter
import api.schemas.rhyme as rhyme_schema

router = APIRouter()

@router.post("/judge", response_model=rhyme_schema.RhymeScore)
async def judge_rhyme(request_body: rhyme_schema.RhymeInput):
    return rhyme_schema.RhymeScore(score=8, title="断頭台", input="パッとしない")