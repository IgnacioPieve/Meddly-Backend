import datetime
import random

import requests
from fastapi import APIRouter
from firebase_admin import auth, messaging
from firebase_admin._auth_utils import UserNotFoundError
from pydantic import BaseModel, EmailStr
from sendgrid import Mail, SendGridAPIClient
from sqlalchemy import insert

import database
from api.appointment.models import Appointment
from api.measurement.models import Measurement
from api.medicine.models import Medicine
from api.user.models import User
from config import FIREBASE_KEY, SENDGRID_CONFIG, WHATSAPP_API_KEY
from database import Base, engine

router = APIRouter(prefix="/dev", tags=["Developer_Tools"])


class UserRequestModel(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {"example": {"email": "test@test.com", "password": "password"}}


@router.post("/get-some-users")
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


@router.get("/status")
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


@router.post("/register")
def register(user: UserRequestModel):
    user = {**user.dict(), "returnSecureToken": True}
    url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={FIREBASE_KEY}"
    response = requests.post(url, json=user)
    try:
        return {"status": "ok", "token": response.json()["idToken"]}
    except KeyError:
        print(response.json())


@router.post("/reset-database")
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"status": "ok"}


@router.post("/send_notification")
def send_notification(
    email: str | None = None,
    phone_number: str | None = None,
    device_id: str | None = None,
):
    def send_email():
        message_constructor = Mail(
            from_email=SENDGRID_CONFIG["email"],
            to_emails=email,
        )
        message_constructor.template_id = "d-5e634cd5cd6548b4b440f188c1d2a40a"
        message_constructor.dynamic_template_data = {
            "hi_message": "Hola usuario de prueba!",
            "message": "mensaje de prueba",
            "subject": "mensaje de prueba",
        }
        sg = SendGridAPIClient(SENDGRID_CONFIG["api_key"])
        response = sg.send(message_constructor)
        print(f"Email sent to {email}. Response: {response.status_code}")

    def send_whatsapp():
        message_data = [{"type": "text", "text": "Mensaje de prueba"}]
        headers = {
            "Authorization": f"Bearer {WHATSAPP_API_KEY}",
            "Content-Type": "application/json",
        }
        body = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": "generic_message",
                "language": {"code": "es"},
                "components": [{"type": "body", "parameters": message_data}],
            },
        }
        response = requests.post(
            "https://graph.facebook.com/v15.0/100370432826961/messages",
            headers=headers,
            json=body,
        )
        print(f"Message Sent via Whatsapp to {phone_number}. Response: {response.text}")

    def send_push():
        message = messaging.Message(
            notification=messaging.Notification(
                title="Titulo de prueba",
                body="Mensaje de prueba",
            ),
            token=device_id,
        )
        response = messaging.send(message)
        print(f"Message Sent via Push to {device_id}. Response {response}")

    if email:
        send_email()
    if phone_number:
        send_whatsapp()
    if device_id:
        send_push()


@router.post("/load-example-data")
async def load_example_data():
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

    db = database.database

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    user_igna = "ignacio.pieve@gmail.com"
    user_igna = await db.fetch_one(
        query=insert(User)
        .values(
            id=assure_user_exists(user_igna),
            email=user_igna,
            first_name="Ignacio",
            last_name="Pieve Roiger",
            height=random.randint(150, 170),
            weight=random.randint(45, 75),
            sex=True,
            birth=datetime.datetime(2000, 2, 10),
            phone="+5493516637217",
            invitation="AAA-1111-AAA",
        )
        .returning(User)
    )

    user_sofi = "soficibello@gmail.com"
    user_sofi = await db.fetch_one(
        query=insert(User)
        .values(
            id=assure_user_exists(user_sofi),
            email=user_sofi,
            first_name="Sofía Florencia",
            last_name="Cibello",
            height=random.randint(150, 170),
            weight=random.randint(45, 75),
            sex=False,
            birth=datetime.datetime(1999, 11, 11),
            phone="+5493512672399",
            invitation="BBB-2222-BBB",
        )
        .returning(User)
    )

    user_loren = "salalorennn@gmail.com"
    user_loren = await db.fetch_one(
        query=insert(User)
        .values(
            id=assure_user_exists(user_loren),
            email=user_loren,
            first_name="Lorenzo",
            last_name="Sala",
            height=random.randint(150, 170),
            weight=random.randint(45, 75),
            sex=True,
            birth=datetime.datetime(1999, 11, 4),
            phone="+5493543572535",
            invitation="CCC-3333-CCC",
        )
        .returning(User)
    )

    # TODO: FIX THIS
    # # Ignacio supervises Lorenzo and Sofía, Sofía supervises Lorenzo, Lorenzo supervises Ignacio
    # user_loren.accept_invitation(user_igna.invitation)
    # user_loren.accept_invitation(user_sofi.invitation)
    #
    # user_sofi.accept_invitation(user_igna.invitation)
    #
    # user_igna.accept_invitation(user_loren.invitation)

    test_medicines = [
        {
            "name": "Ibuprofeno",
            "start_date": datetime.datetime.now(),
            "end_date": datetime.datetime.now() + datetime.timedelta(days=20),
            "stock": 15,
            "stock_warning": 5,
            "presentation": "capsule",
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
            "presentation": "capsule",
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
            "presentation": "liquid",
            "dosis_unit": "mL",
            "dosis": 20,
            "instructions": "Tomarmelo entero",
            "days": [1, 3, 5, 7],
            "hours": ["08:00", "13:00", "20:00"],
        },
    ]
    users = [user_igna, user_sofi, user_loren]
    for test_medicine in test_medicines:
        for user in users:
            await db.execute(
                query=insert(Medicine).values(**test_medicine, user_id=user.id)
            )

    test_appointments = [
        {
            "date": datetime.datetime.now(),
            "name": "Consulta con Cardiólogo",
            "doctor": "Dr. Juan Perez",
            "speciality": "cardiology",
            "location": "Hospital de la ciudad",
            "notes": "Llevar los resultados de los análisis",
        },
        {
            "date": datetime.datetime.now() + datetime.timedelta(days=1),
            "name": "Turno con el neumonologo",
            "doctor": "Dra. Anastasia Rodriguez",
            "speciality": "pulmonology",
            "location": "Av. Santiago Baravino 4238",
        },
        {
            "date": datetime.datetime.now() + datetime.timedelta(days=3),
            "name": "Consulta con el psiquiatra",
            "doctor": "Dr. Pedro Martinez",
            "speciality": "psychiatry",
            "location": "Av. Colón 1234",
            "notes": "Llevar plata, la consulta cuesta caro",
        },
    ]
    for test_appointment in test_appointments:
        for user in users:
            await db.execute(
                query=insert(Appointment).values(**test_appointment, user_id=user.id)
            )

    test_measurements = [
        {
            "date": datetime.datetime.now(),
            "type": "bloodGlucose",
            "unit": "mgPerDL",
            "value": 95.0,
        },
        {
            "date": datetime.datetime.now() + datetime.timedelta(hours=2),
            "type": "bloodPressure",
            "unit": "mmHg",
            "value": 114,
        },
        {
            "date": datetime.datetime.now() + datetime.timedelta(days=1),
            "type": "bloodGlucose",
            "unit": "mgPerDL",
            "value": 100.0,
        },
        {
            "date": datetime.datetime.now() + datetime.timedelta(days=2),
            "type": "bloodGlucose",
            "unit": "mgPerDL",
            "value": 115.0,
        },
        {
            "date": datetime.datetime.now()
            + datetime.timedelta(days=2)
            + datetime.timedelta(hours=2),
            "type": "bloodPressure",
            "unit": "mmHg",
            "value": 102,
        },
        {
            "date": datetime.datetime.now() + datetime.timedelta(days=3),
            "type": "bloodGlucose",
            "unit": "mgPerDL",
            "value": 103.0,
        },
        {
            "date": datetime.datetime.now() + datetime.timedelta(days=4),
            "type": "bloodGlucose",
            "unit": "mgPerDL",
            "value": 235.0,
        },
        {
            "date": datetime.datetime.now() + datetime.timedelta(days=5),
            "type": "bloodGlucose",
            "unit": "mgPerDL",
            "value": 105.0,
        },
    ]
    for test_measurement in test_measurements:
        for user in users:
            await db.execute(
                query=insert(Measurement).values(**test_measurement, user_id=user.id)
            )
