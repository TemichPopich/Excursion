from app.models import TuneModel


class PatchFeedback(TuneModel):
    score: int
    desc: str


class Feedback(PatchFeedback):
    client_id: int
    exc_id: int
