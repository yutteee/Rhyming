from fastapi import APIRouter
import pykakasi
import api.schemas.rhyme as rhyme_schema

kks = pykakasi.kakasi()

router = APIRouter()

def ignoreWord(word):
    return word.replace("ん", "").replace("ー", "").replace("っ", "")

def removeConsonants(input):
    vowels = "aiueo"
    result = ""
    for char in input:
        if char in vowels:
            result += char
    return result

@router.post("/judge", response_model=rhyme_schema.RhymeScore)
async def judge_rhyme(request_body: rhyme_schema.RhymeInput):
    title = kks.convert(request_body.title)
    input = kks.convert(request_body.input)

    hiraTitle = ''.join([item["hira"] for item in title])
    hiraInput = ''.join([item["hira"] for item in input])

    filteredHiraTitle = ignoreWord(hiraTitle)
    filteredHiraInput = ignoreWord(hiraInput)

    # 子音踏みをreturn
    if filteredHiraTitle == filteredHiraInput:
        score = len(filteredHiraTitle) + 3
        return rhyme_schema.RhymeScore(score=score, title=request_body.title, input=request_body.input)

    hiraTitleKakasi = kks.convert(filteredHiraTitle)
    hiraInputKakasi = kks.convert(filteredHiraInput)
    romajiTitle = ''.join([item["hepburn"] for item in hiraTitleKakasi])
    romajiInput = ''.join([item["hepburn"] for item in hiraInputKakasi])

    vowelsTitle = removeConsonants(romajiTitle)
    vowelsInput = removeConsonants(romajiInput)


    print(vowelsTitle)
    print(vowelsInput)
    return rhyme_schema.RhymeScore(score=8, title=request_body.title, input=request_body.input)