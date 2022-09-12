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

    def sms(self):
        """
        Returns a message (str)
        TODO: Complete this description
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
        template_id = "new_supervisor"
        return {
            "template_id": template_id,
            "template_data": [
                {
                    "type": "text",
                    "text": self.supervisor.name
                    if hasattr(self.supervisor, "name")
                    else "",
                }
            ],
        }

    def email(self):
        return {
            "template_id": "d-5e634cd5cd6548b4b440f188c1d2a40a",
            "template_data": {
                "supervisor_name": self.supervisor.name
                if hasattr(self.supervisor, "name")
                else ""
            },
        }

    def sms(self):
        return f"Has añadido a {self.supervisor.name} como supervisor."

    def push(self):
        return {
            'title': 'Nuevo supervisor',
            'body': f'Has añadido a {self.supervisor.name} como supervisor.'
        }
