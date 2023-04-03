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

    # 離れ踏みをreturn
    if filteredHiraTitle[:2] == filteredHiraInput[:2] and filteredHiraTitle[-2:] == filteredHiraInput[-2:]:
        # 最初の何文字があっているかを探索
        n = min(len(filteredHiraTitle), len(filteredHiraInput))
        count = 0
        for i in range(n):
            if filteredHiraTitle[i] == filteredHiraInput[i]:
                count += 1
            else:
                break

        remain = len(filteredHiraTitle) - count
        # 残りの文字で踏めていたら離れ踏み成立
        if filteredHiraTitle[-remain:] == filteredHiraInput[-remain:]:
            score = len(filteredHiraTitle) + 5
            return rhyme_schema.RhymeScore(score=score, title=request_body.title, input=request_body.input)

    hiraTitleKakasi = kks.convert(filteredHiraTitle)
    hiraInputKakasi = kks.convert(filteredHiraInput)
    romajiTitle = ''.join([item["hepburn"] for item in hiraTitleKakasi])
    romajiInput = ''.join([item["hepburn"] for item in hiraInputKakasi])

    vowelsTitle = removeConsonants(romajiTitle)
    vowelsInput = removeConsonants(romajiInput)

    max_length = len(vowelsTitle)

    for length in range(max_length, 0, -1): # 最大値からループ
        if length == 1:
            return rhyme_schema.RhymeScore(score=0, title=request_body.title, input=request_body.input)
        # 母音が全て一致している場合
        substring = vowelsTitle[:length]
        if substring in vowelsInput:
            return rhyme_schema.RhymeScore(score=length, title=request_body.title, input=request_body.input)
        # 母音が一部一致している場合
        for start in range(length - 1):
            substring = vowelsTitle[start:(length+start)]
            if substring in vowelsInput:
                return rhyme_schema.RhymeScore(score=length, title=request_body.title, input=request_body.input)
