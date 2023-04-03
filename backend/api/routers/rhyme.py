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

    tmpTitle = ''.join([item["hira"] for item in title])
    tmpInput = ''.join([item["hira"] for item in input])
    hiraTitleKakasi = kks.convert(ignoreWord(tmpTitle))
    hiraInputKakasi = kks.convert(ignoreWord(tmpInput))

    romajiTitle = ''.join([item["hepburn"] for item in hiraTitleKakasi])
    romajiInput = ''.join([item["hepburn"] for item in hiraInputKakasi])

    vowelsTitle = removeConsonants(romajiTitle)
    vowelsInput = removeConsonants(romajiInput)
    print(vowelsTitle)
    print(vowelsInput)
    return rhyme_schema.RhymeScore(score=8, title=request_body.title, input=request_body.input)