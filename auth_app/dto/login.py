from dataclasses import dataclass


@dataclass
class LoginDto:
    username: str
    password: str
