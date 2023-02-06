class Message:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

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


class NewSupervisorMessage(Message):
    def __init__(self, **kwargs):
        self.supervisor = kwargs["supervisor"]
        super().__init__(**kwargs)

    def whatsapp(self):
        if self.supervisor.first_name:
            return {
                "message": f"Felicitaciones! Has añadido a {self.supervisor.first_name} como supervisor. "
                f"Recuerda verificar tus supervisores desde la app",
            }
        return {
            "message": "Felicitaciones! Has añadido a un nuevo supervisor. "
            "Recuerda verificar tus supervisores desde la app",
        }

    def email(self):
        if self.supervisor.first_name:
            return {
                "subject": f"Has añadido a {self.supervisor.first_name} como supervisor.",
                "message": f"Felicitaciones! Has añadido a {self.supervisor.first_name} como supervisor. "
                f"Recuerda verificar tus supervisores desde la app.",
            }
        return {
            "subject": "Has añadido a un nuevo supervisor.",
            "message": "Felicitaciones! Has añadido a un nuevo supervisor. "
            "Recuerda verificar tus supervisores desde la app.",
        }

    def push(self):
        return {
            "title": "Nuevo supervisor",
            "body": f"Has añadido a {self.supervisor.first_name} como supervisor.",
        }


class NewSupervisedMessage(Message):
    def __init__(self, **kwargs):
        self.supervised = kwargs["supervised"]
        super().__init__(**kwargs)

    def whatsapp(self):
        if self.supervised.first_name:
            return {
                "message": f"Felicitaciones! Has añadido a {self.supervised.first_name} como supervisado. "
                f"Recuerda verificar tus supervisados desde la app",
            }
        return {
            "message": "Felicitaciones! Has añadido a un nuevo supervisado. "
            "Recuerda verificar tus supervisados desde la app",
        }

    def email(self):
        if self.supervised.first_name:
            return {
                "subject": f"Has añadido a {self.supervised.first_name} como supervisado.",
                "message": f"Felicitaciones! Has añadido a {self.supervised.first_name} como supervisado. "
                f"Recuerda verificar tus supervisados desde la app.",
            }
        return {
            "subject": "Has añadido a un nuevo supervisado.",
            "message": "Felicitaciones! Has añadido a un nuevo supervisado. "
            "Recuerda verificar tus supervisados desde la app.",
        }

    def push(self):
        return {
            "title": "Nuevo supervisado",
            "body": f"Has añadido a {self.supervised.first_name} como supervisado.",
        }
