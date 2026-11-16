from pydantic import BaseModel, Field


class SignupRequest(BaseModel):
    """The sign-up form."""

    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    """The login form."""

    email: str
    password: str


class MessageResponse(BaseModel):
    """A short reply from the bank."""

    message: str