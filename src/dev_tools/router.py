import datetime
import random
from user_calendar.models.appointment import Appointment
from user_calendar.models.measurement import Measurement
from user_calendar.models.medicine import Medicine

import requests
from fastapi import APIRouter, Depends
from firebase_admin import auth
from firebase_admin._auth_utils import UserNotFoundError
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from config import FIREBASE_KEY
from database import Base, engine, get_db
from user.models import User

router = APIRouter(prefix="/dev", tags=["Developer_Tools"])


class UserRequestModel(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {"example": {"email": "test@test.com", "password": "password"}}


@router.post("/get-some-users", include_in_schema=False)
@router.post("/get-some-users/")
def get_some_users():
    users = [
        "user1@gmail.com",
        "user2@gmail.com",
        "ignacio.pieve@gmail.com",
        "soficibello@gmail.com",
    ]
    tokens = {}
    for user in users:
        user_data = {"email": user, "password": "password", "returnSecureToken": True}
        url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={FIREBASE_KEY}"
        response = requests.post(url, json=user_data)
        try:
            tokens[user] = response.json()["idToken"]
        except KeyError:
            url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={FIREBASE_KEY}"
            response = requests.post(url, json=user_data)
            tokens[user] = response.json()["idToken"]

    return tokens


@router.get("/status", include_in_schema=False)
@router.get("/status/")
def get_status():
    """Get status of messaging server."""
    return {"status": "running"}


@router.post("/login", include_in_schema=False)
@router.post("/login/")
def login(user: UserRequestModel):
    user = {**user.dict(), "returnSecureToken": True}
    url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={FIREBASE_KEY}"
    response = requests.post(url, json=user)
    try:
        return {"status": "ok", "token": response.json()["idToken"]}
    except KeyError:
        print(response.json())


@router.post("/register", include_in_schema=False)
@router.post("/register/")
def register(user: UserRequestModel):
    user = {**user.dict(), "returnSecureToken": True}
    url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={FIREBASE_KEY}"
    response = requests.post(url, json=user)
    try:
        return {"status": "ok", "token": response.json()["idToken"]}
    except KeyError:
        print(response.json())


@router.post("/reset-database", include_in_schema=False)
@router.post("/reset-database/")
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"status": "ok"}


@router.post("/load-example-data", include_in_schema=False)
@router.post("/load-example-data/")
def load_example_data(db: Session = Depends(get_db)):
    def assure_user_exists(email):
        try:
            return auth.get_user_by_email(email).uid
        except UserNotFoundError:
            user_data = {
                "email": email,
                "password": "password",
                "returnSecureToken": True,
            }
            url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={FIREBASE_KEY}"
            return requests.post(url, json=user_data).json()["localId"]

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    user_igna = "ignacio.pieve@gmail.com"
    user_igna = User(
        db,
        id=assure_user_exists(user_igna),
        email=user_igna,
        first_name="Ignacio",
        last_name="Pieve Roiger",
        height=random.randint(150, 170),
        weight=random.randint(45, 75),
        sex=True,
        birth=datetime.datetime(2000, 2, 10),
        phone="+5493516637217",
    )
    user_igna.create()

    user_sofi = "soficibello@gmail.com"
    user_sofi = User(
        db,
        id=assure_user_exists(user_sofi),
        email=user_sofi,
        first_name="Sofía Florencia",
        last_name="Cibello",
        height=random.randint(150, 170),
        weight=random.randint(45, 75),
        sex=False,
        birth=datetime.datetime(1999, 11, 11),
        phone="+5493512672399",
    )
    user_sofi.create()

    user_loren = "salalorennn@gmail.com"
    user_loren = User(
        db,
        id=assure_user_exists(user_loren),
        email=user_loren,
        first_name="Lorenzo",
        last_name="Sala",
        height=random.randint(150, 170),
        weight=random.randint(45, 75),
        sex=True,
        birth=datetime.datetime(1999, 11, 4),
        phone="+5493543572535",
    )
    user_loren.create()

    # Ignacio supervises Lorenzo and Sofía, Sofía supervises Lorenzo, Lorenzo supervises Ignacio
    user_loren.accept_invitation(user_igna.invitation)
    user_loren.accept_invitation(user_sofi.invitation)

    user_sofi.accept_invitation(user_igna.invitation)

    user_igna.accept_invitation(user_loren.invitation)

    test_medicines = [
        {
            "name": "Ibuprofeno",
            "start_date": datetime.datetime.now(),
            "end_date": datetime.datetime.now() + datetime.timedelta(days=20),
            "stock": 15,
            "stock_warning": 5,
            "presentation": "Pastilla",
            "dosis_unit": "mg",
            "dosis": 1.5,
            "instructions": "Disolver la pastilla en agua",
            "interval": 3,
            "hours": ["08:00", "11:00", "18:00"],
        },
        {
            "name": "Paracetamol",
            "start_date": datetime.datetime.now(),
            "end_date": datetime.datetime.now() + datetime.timedelta(days=25),
            "stock": 20,
            "stock_warning": 5,
            "presentation": "Pastilla",
            "dosis_unit": "mg",
            "dosis": 1.5,
            "instructions": "Consumir cuando me duela la cabeza",
        },
        {
            "name": "Amoxidal",
            "start_date": datetime.datetime.now(),
            "end_date": datetime.datetime.now() + datetime.timedelta(days=30),
            "stock": 20,
            "stock_warning": 4,
            "presentation": "Líquido",
            "dosis_unit": "ml",
            "dosis": 20,
            "instructions": "Tomarmelo entero",
            "days": [1, 3, 5, 7],
            "hours": ["08:00", "13:00", "20:00"],
        },
    ]
    users = [user_igna, user_sofi, user_loren]
    for test_medicine in test_medicines:
        for user in users:
            medicine = Medicine(db, **test_medicine, user_id=user.id)
            medicine.create()

    test_appointments = [
        {
            "date": datetime.datetime.now(),
            "name": "Consulta con Cardiólogo",
            "doctor": "Dr. Juan Perez",
            "speciality": "Cardiología",
            "location": "Hospital de la ciudad",
            "notes": "Llevar los resultados de los análisis",
        },
        {
            "date": datetime.datetime.now() + datetime.timedelta(days=1),
            "name": "Turno con el dentista",
            "doctor": "Dra. Anastasia Rodriguez",
            "speciality": "Dentista",
            "location": "Av. Santiago Baravino 4238",
        },
        {
            "date": datetime.datetime.now() + datetime.timedelta(days=3),
            "name": "Consulta con el psicólogo",
            "doctor": "Dr. Pedro Martinez",
            "speciality": "Psicología",
            "location": "Av. Colón 1234",
            "notes": "Llevar plata, la consulta cuesta caro",
        },
    ]
    for test_appointment in test_appointments:
        for user in users:
            appointment = Appointment(db, **test_appointment, user_id=user.id)
            appointment.create()

    test_measurements = [
        {
            "date": datetime.datetime.now(),
            "type": "Glucosa",
            "unit": "mg/dL",
            "value": 95.0,
        },
        {
            "date": datetime.datetime.now() + datetime.timedelta(hours=2),
            "type": "Presión Arterial",
            "unit": "mmHg",
            "value": 114,
        },
        {
            "date": datetime.datetime.now() + datetime.timedelta(days=1),
            "type": "Glucosa",
            "unit": "mg/dL",
            "value": 100.0,
        },
        {
            "date": datetime.datetime.now() + datetime.timedelta(days=2),
            "type": "Glucosa",
            "unit": "mg/dL",
            "value": 115.0,
        },
        {
            "date": datetime.datetime.now()
            + datetime.timedelta(days=2)
            + datetime.timedelta(hours=2),
            "type": "Presión Arterial",
            "unit": "mmHg",
            "value": 102,
        },
        {
            "date": datetime.datetime.now() + datetime.timedelta(days=3),
            "type": "Glucosa",
            "unit": "mg/dL",
            "value": 103.0,
        },
        {
            "date": datetime.datetime.now() + datetime.timedelta(days=4),
            "type": "Glucosa",
            "unit": "mg/dL",
            "value": 235.0,
        },
        {
            "date": datetime.datetime.now() + datetime.timedelta(days=5),
            "type": "Glucosa",
            "unit": "mg/dL",
            "value": 105.0,
        },
    ]
    for test_measurement in test_measurements:
        for user in users:
            measurement = Measurement(db, **test_measurement, user_id=user.id)
            measurement.create()
