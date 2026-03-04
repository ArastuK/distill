from pydantic import BaseModel


class Timestamp(BaseModel):
    start: float
    end: float

    def format(self) -> str:
        def _fmt(seconds: float) -> str:
            h = int(seconds // 3600)
            m = int((seconds % 3600) // 60)
            s = int(seconds % 60)
            if h > 0:
                return f"{h}:{m:02d}:{s:02d}"
            return f"{m}:{s:02d}"

        return f"{_fmt(self.start)} - {_fmt(self.end)}"


class Section(BaseModel):
    title: str
    summary: str
    key_points: list[str]
    notable_quotes: list[str]
    timestamp: Timestamp


class ConceptLink(BaseModel):
    source: str
    target: str
    relationship: str


class ConceptMap(BaseModel):
    topics: list[str]
    links: list[ConceptLink]


class DistillResult(BaseModel):
    title: str
    source_url: str
    duration: str
    total_sections: int
    overview: str
    sections: list[Section]
    concept_map: ConceptMap
    key_takeaways: list[str]
