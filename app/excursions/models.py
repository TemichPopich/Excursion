import datetime
from app.models import TuneModel


class PostExcursion(TuneModel):
    country: str
    city: str
    date: datetime.date
    price: float
    people_count: int
    child_presence: bool
    path_diff: str
    desc: str
    name: str
    score: float
    feedback_count: int


class Excursion(PostExcursion):
    id: int
    guide_id: int
