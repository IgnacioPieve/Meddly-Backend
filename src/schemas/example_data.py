import datetime
import random
import string

from faker import Faker


def generate_invitation():
    generated_code = []
    for k in [3, 4, 3]:
        generated_code.append("".join(random.choices(string.ascii_uppercase, k=k)))
    generated_code = "-".join(generated_code).upper()
    return generated_code


possible_preferences = ["email", "whatsapp", "sms", "push"]

example_profile = Faker()
example_profile.id = lambda: "".join(
    random.choices(string.ascii_letters + string.digits, k=28)
)
example_profile.avatar = lambda: f"avatar{random.randint(1, 4)}"
example_profile.created_at = lambda: datetime.datetime.now() - datetime.timedelta(
    seconds=random.randint(86400, 86400 * 31)
)
example_profile.updated_at = lambda: datetime.datetime.now()
example_profile.invitation = generate_invitation
example_profile.sex = lambda: random.choice(["M", "F"])
example_profile.height = lambda: round(random.uniform(1.6, 1.8), 2)
example_profile.weight = lambda: random.randint(50, 80)
example_profile.notification_preferences = lambda: random.sample(
    possible_preferences, random.randint(1, len(possible_preferences))
)
example_profile.phone = lambda: int(f'351{random.randint(1111111, 9999999)}')
