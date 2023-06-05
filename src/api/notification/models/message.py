class Message:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def whatsapp(self):
        """
        Returns a message: str on a dict.
        {
            "message": "Some message"
        }
        """
        raise Exception("NotImplementedException")

    def email(self):
        """
        Returns a message: str and a subject: str on a dict.
        {
            "subject": "Some subject",
            "message": "Some message"
        }
        """
        raise Exception("NotImplementedException")

    def push(self):
        """
        Returns the title and the body on a dict.
        {
            "title": "Push Title",
            "body": "Push Body"
        }
        """
        raise Exception("NotImplementedException")

    def send(self):
        """
        Sends the message to the user.
        """
        raise Exception("NotImplementedException")


class NewSupervisorMessage(Message):
    def whatsapp(self):
        return {
            "message": f"Felicitaciones! Has añadido a {self.supervisor.get_fullname()} como supervisor. "
            f"Recuerda verificar tus supervisores desde la app",
        }

    def email(self):
        return {
            "subject": f"Has añadido a {self.supervisor.get_fullname()} como supervisor.",
            "message": f"Felicitaciones! Has añadido a {self.supervisor.get_fullname()} como supervisor. "
            f"Recuerda verificar tus supervisores desde la app.",
        }

    def push(self):
        return {
            "title": "Nuevo supervisor",
            "body": f"Has añadido a {self.supervisor.get_fullname()} como supervisor.",
        }


class NewSupervisedMessage(Message):
    def whatsapp(self):
        return {
            "message": f"Felicitaciones! Has añadido a {self.supervised.get_fullname()} como supervisado. "
            f"Recuerda verificar tus supervisados desde la app",
        }

    def email(self):
        return {
            "subject": f"Has añadido a {self.supervised.get_fullname()} como supervisado.",
            "message": f"Felicitaciones! Has añadido a {self.supervised.get_fullname()} como supervisado. "
            f"Recuerda verificar tus supervisados desde la app.",
        }

    def push(self):
        return {
            "title": "Nuevo supervisado",
            "body": f"Has añadido a {self.supervised.get_fullname()} como supervisado.",
        }


class TodayUserAppointments(Message):
    def whatsapp(self):
        m = f"Buenos días {self.user.get_fullname()}! Recuerda que tienes las siguientes citas hoy:\r\n\r\n<br>"
        for appointment in self.appointments:
            m += f'- {appointment.name} a las {appointment.date.strftime("%H:%M")}\r\n'
        m += f"\r\nRecuerda que puedes ver tus citas desde la app."
        return {"message": m}

    def email(self):
        m = f"Recuerda que tienes las siguientes citas hoy:<br><br>"
        for appointment in self.appointments:
            m += f'- {appointment.name} a las {appointment.date.strftime("%H:%M")}<br>'
        m += f"<br>Puedes ver información más detallada sobre tus citas médicas de hoy desde la app."
        return {"subject": f"Recordatorio de citas médicas", "message": m}

    def push(self):
        return {
            "title": "Recordatorio de Meddly",
            "body": f"Buenos días {self.user.get_fullname()}! Ingresa a la app para ver tus citas médicas de hoy",
        }


class TodayUserMedicines(Message):
    def whatsapp(self):
        m = f"Buenos días {self.user.get_fullname()}! Recuerda que tienes que tomar los siguientes medicamentos hoy:\n\n"
        for medicine in self.medicines.values():
            m += f'- {medicine["name"]} a las {", ".join(medicine["hours"])}\n'
        m += "\nPuedes ver información más detallada sobre sus medicamentos de hoy desde la app."
        return {"message": m}

    def email(self):
        m = f"Buenos días! Recuerda que tienes que tomar los siguientes medicamentos hoy:<br><br>"
        for medicine in self.medicines.values():
            m += f'- <b>{medicine["name"]}</b> a las <b>{", ".join(medicine["hours"])}</b>.<br>'
        m += f"<br>Puedes ver información más detallada sobre tus medicamentos de hoy desde la app."
        return {"subject": f"Recordatorio de medicamentos", "message": m}

    def push(self):
        return {
            "title": "Recordatorio de Meddly",
            "body": f"Buenos días {self.user.get_fullname()}! Ingresa a la app para ver tus medicamentos de hoy",
        }


class YesterdarUserDidntTakeMedicine(Message):
    def whatsapp(self):
        m = f"Buenos días {self.user.get_fullname()}! Recuerda que ayer no tomaste los siguientes medicamentos:\n\n"
        for medicine in self.medicines.values():
            m += f'- {medicine["name"]} a las {", ".join(medicine["hours"])}\n'
        return {"message": m}

    def email(self):
        m = f"Buenos días! Recuerda que ayer no tomaste los siguientes medicamentos:<br><br>"
        for medicine in self.medicines.values():
            m += f'- <b>{medicine["name"]}</b> a las <b>{", ".join(medicine["hours"])}</b><br>'
        m += f"<br>Recuerda que puedes ver tus medicamentos desde la app."
        return {"subject": f"Recordatorio de medicamentos", "message": m}

    def push(self):
        return {
            "title": "Recordatorio de Meddly",
            "body": f"Buenos días {self.user.get_fullname()}! Ingresa a la app para ver "
            f"tus medicamentos no consumidos de ayer.",
        }


# class TodaySupervisedAppointments(Message):
#     def __init__(self, user, supervised, **kwargs):
#         self.user = User(**user)
#         self.supervised = User(**supervised)
#
#         self.supervised_appointments = await get_appointments(
#             self.supervised,
#             datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
#             datetime.now().replace(hour=23, minute=59, second=59, microsecond=0),
#         )
#
#         super().__init__(**kwargs)
#
#     def whatsapp(self):
#         m = f"Buenos días {self.user.get_fullname()}! Recuerda que hoy {self.supervised.get_fullname()} tiene las siguientes citas médicas:\n\n"
#         for appointment in self.supervised_appointments:
#             m += f'- {appointment.name} a las {appointment.date.strftime("%H:%M")}\n'
#         return {"message": m}
#
#     def email(self):
#         m = f"Buenos días {self.user.get_fullname()}! Recuerda que hoy {self.supervised.get_fullname()} tiene las siguientes citas médicas:\n\n"
#         for appointment in self.supervised_appointments:
#             m += f'- {appointment.name} a las {appointment.date.strftime("%H:%M")}\n'
#         return {"subject": f"Recordatorio de citas médicas", "message": m}
#
#     def push(self):
#         return {
#             "title": "Recordatorio de Meddly",
#             "body": f"Buenos días {self.user.get_fullname()}! Ingresa a la app para ver "
#             f"las citas médicas de {self.supervised.get_fullname()} de hoy.",
#         }
#
#
# class TodaySupervisedMedicines(Message):
#     def __init__(self, user, supervised, **kwargs):
#         self.user = User(**user)
#         self.supervised = User(**supervised)
#
#         today_consumptions = await get_consumptions(
#             self.supervised,
#             datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
#             datetime.now().replace(hour=23, minute=59, second=59, microsecond=0),
#         )
#         self.today_medicines = {}
#         for consumption in today_consumptions:
#             if consumption.medicine.id not in self.today_medicines:
#                 self.today_medicines[consumption.medicine.id] = {
#                     "name": await get_medicine(
#                         self.supervised, consumption.medicine.id
#                     ),
#                     "hours": [],
#                 }
#             self.today_medicines[consumption.medicine.id]["hours"].append(
#                 consumption.date.strftime("%H:%M")
#             )
#
#         super().__init__(**kwargs)
#
#     def whatsapp(self):
#         m = f"Buenos días {self.user.get_fullname()}! Recuerda que hoy {self.supervised.get_fullname()} tiene que tomar los siguientes medicamentos:\n\n"
#         for medicine in self.today_medicines:
#             m += f'- {medicine["name"]} a las {", ".join(medicine["hours"])}\n'
#         return {"message": m}
#
#     def email(self):
#         m = f"Buenos días {self.user.get_fullname()}! Recuerda que hoy {self.supervised.get_fullname()} tiene que tomar los siguientes medicamentos:\n\n"
#         for medicine in self.today_medicines:
#             m += f'- {medicine["name"]} a las {", ".join(medicine["hours"])}\n'
#         return {"subject": f"Recordatorio de medicamentos", "message": m}
#
#     def push(self):
#         return {
#             "title": "Recordatorio de Meddly",
#             "body": f"Buenos días {self.user.get_fullname()}! Ingresa a la app para ver "
#             f"los medicamentos de {self.supervised.get_fullname()} de hoy.",
#         }
#
#
# class YesterdaySupervisedDidntTakeMedicine(Message):
#     def __init__(self, user, supervised, **kwargs):
#         self.user = User(**user)
#         self.supervised = User(**supervised)
#
#         yesterday_consumptions = await get_consumptions(
#             self.supervised,
#             datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
#             - timedelta(days=1),
#             datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
#             - timedelta(days=1),
#         )
#         self.yesterday_medicines = {}
#         for consumption in yesterday_consumptions:
#             if consumption.consumed:
#                 if consumption.medicine.id not in self.yesterday_medicines:
#                     self.yesterday_medicines[consumption.medicine.id] = {
#                         "name": await get_medicine(
#                             self.supervised, consumption.medicine.id
#                         ),
#                         "hours": [],
#                     }
#                 self.yesterday_medicines[consumption.medicine.id]["hours"].append(
#                     consumption.date.strftime("%H:%M")
#                 )
#
#         super().__init__(**kwargs)
#
#     def whatsapp(self):
#         m = f"Buenos días {self.user.get_fullname()}! Recuerda que ayer {self.supervised.get_fullname()} no tomó los siguientes medicamentos:\n\n"
#         for medicine in self.yesterday_medicines:
#             m += f'- {medicine["name"]} a las {", ".join(medicine["hours"])}\n'
#         return {"message": m}
#
#     def email(self):
#         m = f"Buenos días {self.user.get_fullname()}! Recuerda que ayer {self.supervised.get_fullname()} no tomó los siguientes medicamentos:\n\n"
#         for medicine in self.yesterday_medicines:
#             m += f'- {medicine["name"]} a las {", ".join(medicine["hours"])}\n'
#         return {"subject": f"Recordatorio de medicamentos", "message": m}
#
#     def push(self):
#         return {
#             "title": "Recordatorio de Meddly",
#             "body": f"Buenos días {self.user.get_fullname()}! Ingresa a la app para ver "
#             f"los medicamentos no consumidos de {self.supervised.get_fullname()} de ayer.",
#         }
