from dataclasses import dataclass


@dataclass
class RegisterDto:
    username: str
    email: str
    password: str
