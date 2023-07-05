class Message:
    type: str

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
    type = "supervisors"

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
    type = "supervisors"

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
    type = "appointment"

    def whatsapp(self):
        m = f"Buenos días {self.user.get_fullname()}!\n\n"
        if self.appointments:
            m += "\nRecuerda que tienes las siguientes citas hoy:\n"
            for appointment in self.appointments:
                m += (
                    f'- {appointment.name} a las {appointment.date.strftime("%H:%M")}\n'
                )
        if self.supervised_appointments:
            m += "\nTus supervisados tienen las siguientes citas hoy:\n"
            for supervised in self.supervised_appointments:
                m += f'\n{supervised["name"]}:\n'
                for appointment in supervised["appointments"]:
                    m += f'- {appointment.name} a las {appointment.date.strftime("%H:%M")}\n'
        m += f"\r\nRecuerda que puedes ver tus citas desde la app."
        return {"message": m}

    def email(self):
        m = ""
        if self.appointments:
            m = f"Recuerda que tienes las siguientes citas hoy:<br><br>"
            for appointment in self.appointments:
                m += f'- <em>{appointment.name}</em> a las {appointment.date.strftime("%H:%M")}<br>'
        if self.supervised_appointments:
            m += f"<br><br>Tus supervisados tienen las siguientes citas hoy:<br>"
            for supervised in self.supervised_appointments:
                m += f'<br><b>{supervised["name"]}:</b><br>'
                for appointment in supervised["appointments"]:
                    m += f'- <em>{appointment.name}</em> a las {appointment.date.strftime("%H:%M")}<br>'
        m += f"<br>Puedes ver información más detallada sobre las citas médicas de hoy desde la app."
        return {"subject": f"Recordatorio de citas médicas", "message": m}

    def push(self):
        return {
            "title": "Recordatorio de Meddly",
            "body": f"Buenos días {self.user.get_fullname()}! Ingresa a la app para ver tus citas médicas de hoy",
        }


class TodayUserMedicines(Message):
    type = "medicine"

    def whatsapp(self):
        m = f"Buenos días {self.user.get_fullname()}!\n"
        if self.medicines:
            m += "\nRecuerda que tienes que tomar los siguientes medicamentos hoy:\n"
            for medicine in self.medicines.values():
                m += f'- {medicine["name"]} a las {", ".join(medicine["hours"])}\n'
        if self.supervised_medicines:
            m += (
                "\nTus supervisados tienen que tomar los siguientes medicamentos hoy:\n"
            )
            for supervised in self.supervised_medicines:
                m += f'\n{supervised["name"]}:\n'
                for medicine in supervised["medicines"].values():
                    m += f'- {medicine["name"]} a las {", ".join(medicine["hours"])}\n'
        m += "\nPuedes ver información más detallada sobre sus medicamentos de hoy desde la app."
        return {"message": m}

    def email(self):
        m = ""
        if self.medicines:
            m = f"Recuerda que tienes que tomar los siguientes medicamentos hoy:<br><br>"
            for medicine in self.medicines.values():
                m += f'- <em>{medicine["name"]}</em> a las {", ".join(medicine["hours"])}<br>'
        if self.supervised_medicines:
            m += f"<br><br>Tus supervisados tienen que tomar los siguientes medicamentos hoy:<br>"
            for supervised in self.supervised_medicines:
                m += f'<br><b>{supervised["name"]}:</b><br>'
                for medicine in supervised["medicines"].values():
                    m += f'- <em>{medicine["name"]}</em> a las {", ".join(medicine["hours"])}<br>'
        m += f"<br>Puedes ver información más detallada sobre sus medicamentos de hoy desde la app."
        return {"subject": f"Recordatorio de medicamentos", "message": m}

    def push(self):
        return {
            "title": "Recordatorio de Meddly",
            "body": f"Buenos días {self.user.get_fullname()}! Ingresa a la app para ver los medicamentos de hoy",
        }


class YesterdarUserDidntTakeMedicine(Message):
    type = "medicine"

    def whatsapp(self):
        m = f"Buenos días {self.user.get_fullname()}!\n"
        if self.medicines:
            m += "\nRecuerda que ayer no tomaste los siguientes medicamentos:\n"
            for medicine in self.medicines.values():
                m += f'- {medicine["name"]} a las {", ".join(medicine["hours"])}\n'
        if self.supervised_medicines:
            m += "\nTus supervisados no tomaron los siguientes medicamentos ayer:\n"
            for supervised in self.supervised_medicines:
                m += f'\n{supervised["name"]}:\n'
                for medicine in supervised["medicines"].values():
                    m += f'- {medicine["name"]} a las {", ".join(medicine["hours"])}\n'
        m += "\nPuedes ver información más detallada sobre sus medicamentos de ayer desde la app."
        return {"message": m}

    def email(self):
        m = ""
        if self.medicines:
            m = f"Recuerda que ayer no tomaste los siguientes medicamentos:<br><br>"
            for medicine in self.medicines.values():
                m += f'- <em>{medicine["name"]}</em> a las {", ".join(medicine["hours"])}<br>'
        if self.supervised_medicines:
            m += f"<br><br>Tus supervisados no tomaron los siguientes medicamentos ayer:<br>"
            for supervised in self.supervised_medicines:
                m += f'<br><b>{supervised["name"]}:</b><br>'
                for medicine in supervised["medicines"].values():
                    m += f'- <em>{medicine["name"]}</em> a las {", ".join(medicine["hours"])}<br>'
        m += f"<br>Puedes ver información más detallada sobre sus medicamentos de ayer desde la app."
        return {"subject": f"Recordatorio de medicamentos", "message": m}

    def push(self):
        return {
            "title": "Recordatorio de Meddly",
            "body": f"Buenos días {self.user.get_fullname()}! Ingresa a la app para ver "
            f"los medicamentos no consumidos de ayer.",
        }


class LowStockMessage(Message):
    type = "medicine"

    def whatsapp(self):
        return {
            "message": f"El medicamento {self.medicine.name} está por agotarse. "
            f"Recuerda evitar que se agote para no interrumpir el tratamiento."
        }

    def email(self):
        return {
            "subject": f"Medicamento por agotarse",
            "message": f"El medicamento {self.medicine.name} está por agotarse. "
            f"Recuerda evitar que se agote para no interrumpir el tratamiento.",
        }

    def push(self):
        return {
            "title": "Medicamento por agotarse",
            "body": f"El medicamento {self.medicine.name} está por agotarse. "
            f"Recuerda evitar que se agote para no interrumpir el tratamiento.",
        }


class LowStockFromSupervisedUserMessage(Message):
    type = "medicine"

    def whatsapp(self):
        return {
            "message": f"El medicamento {self.medicine.name} de {self.supervised_user.get_fullname()} está por agotarse. "
            f"Recuerda evitar que se agote para no interrumpir el tratamiento."
        }

    def email(self):
        return {
            "subject": f"Medicamento por agotarse",
            "message": f"El medicamento {self.medicine.name} de {self.supervised_user.get_fullname()} está por agotarse. "
            f"Recuerda evitar que se agote para no interrumpir el tratamiento.",
        }

    def push(self):
        return {
            "title": "Medicamento por agotarse",
            "body": f"El medicamento {self.medicine.name} de {self.supervised_user.get_fullname()} está por agotarse. "
            f"Recuerda evitar que se agote para no interrumpir el tratamiento.",
        }
