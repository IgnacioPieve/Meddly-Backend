class Message:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def whatsapp(self):
        """
        Returns a message (str)
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

    def sms(self):
        """
        Returns a message (str)
        """
        raise Exception("NotImplementedException")

    def push(self):
        raise Exception("NotImplementedException")


class NewSupervisorMessage(Message):
    def __init__(self, **kwargs):
        self.supervisor = kwargs["supervisor"]
        super().__init__(**kwargs)

    def whatsapp(self):
        if hasattr(self.supervisor, 'name'):
            return f'Has añadido a {self.supervisor.name} como supervisor.'
        else:
            return f'Has añadido a un nuevo supervisor.'

    def email(self):
        template_id = 'd-5e634cd5cd6548b4b440f188c1d2a40a'
        return {
            "template_id": template_id,
            "template_data": {
                "supervisor_name": self.supervisor.name if hasattr(self.supervisor, 'name') else ""
            }
        }

    def sms(self):
        return f'Has añadido a {self.supervisor.name} como supervisor.'

    def push(self):
        raise Exception("NotImplementedException")
