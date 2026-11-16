from fastapi import FastAPI, HTTPException, status

from database import Database
from schemas import LoginRequest, MessageResponse, SignupRequest
from security import PasswordService
from services import UserService


class GateWatchApp:
    """The main building of GateWatch."""

    def __init__(self):
        self.app = FastAPI(title="GateWatch")
        database = Database()
        database.create_tables()
        self.users = UserService(database, PasswordService())
        self._add_routes()

    def _add_routes(self):
        self.app.get("/health")(self.health)
        self.app.post("/signup", status_code=status.HTTP_201_CREATED)(self.signup)
        self.app.post("/login")(self.login)

    def health(self):
        return {"status": "GateWatch is alive"}

    def signup(self, form: SignupRequest) -> MessageResponse:
        user = self.users.register(form.email, form.password)
        if user is None:
            raise HTTPException(status_code=409, detail="Email already registered")
        return MessageResponse(message="Account created")

    def login(self, form: LoginRequest) -> MessageResponse:
        user = self.users.authenticate(form.email, form.password)
        if user is None:
            raise HTTPException(status_code=401, detail="Wrong email or password")
        return MessageResponse(message="Login successful")


app = GateWatchApp().app