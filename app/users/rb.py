class RBUser:
    def __init__(
        self,
        phone: str | None = None,
        username: str | None = None,
        email: str | None = None,
    ):
        self.phone = phone
        self.username = username
        self.email = email

    def to_dict(self) -> dict:
        data = {"phone": self.phone, "username": self.username, "email": self.email}

        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data
