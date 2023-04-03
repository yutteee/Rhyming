from pydantic import BaseModel, Field

class RhymeBase(BaseModel):
    title: str = Field(example="ストライク")
    input: str = Field(example="すっと入る")

# req
class RhymeInput(RhymeBase):
    pass

# res
class RhymeScore(RhymeBase):
    score: int = Field(0, example=2)