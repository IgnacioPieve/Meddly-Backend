class Message:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def whatsapp(self):
        """
        Returns a message (str)
        TODO: Complete this description
        """
        raise Exception("NotImplementedException")

    def email(self):
        """
        Returns the template_id and the template_data (dict).
        {
            "template_id": "",
            "template_data": {
                "example": "example"
            }
        }
        """
        raise Exception("NotImplementedException")

    def push(self):
        """
        Returns the title and the body (dict).
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
        if hasattr(self.supervisor, "name"):
            return {
                "message": f"Felicitaciones! Has añadido a {self.supervisor.name} como supervisor. "
                           f"Recuerda verificar tus supervisores desde la app",
            }
        return {
            "subject": "Has añadido a un nuevo supervisor.",
            "message": "Felicitaciones! Has añadido a un nuevo supervisor. "
                       "Recuerda verificar tus supervisores desde la app",
        }

    def email(self):
        if hasattr(self.supervisor, "name"):
            return {
                "subject": f"Has añadido a {self.supervisor.name} como supervisor.",
                "message": f"Felicitaciones! Has añadido a {self.supervisor.name} como supervisor. "
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
            "body": f"Has añadido a {self.supervisor.name} como supervisor.",
        }
