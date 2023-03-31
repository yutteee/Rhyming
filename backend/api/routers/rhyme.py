from fastapi import APIRouter

router = APIRouter()

@router.post("/judge")
async def judge_rhyme():
    pass