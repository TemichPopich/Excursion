import datetime


class RBExcursion:
    def __init__(
        self,
        country: str | None = None,
        city: str | None = None,
        date: datetime.date | None = None,
        name: str | None = None,
        path_diff: str | None = None,
    ):
        self.country = country
        self.city = city
        self.date = date
        self.name = name
        self.path_diff = path_diff

    def to_dict(self) -> dict:
        data = {
            "country": self.country,
            "city": self.city,
            "date": self.date,
            "name": self.name,
            "path_diff": self.path_diff,
        }

        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data
