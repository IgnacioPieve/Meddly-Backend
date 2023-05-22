import base64
import datetime
import io

import jinja2
import pdfkit
import PyPDF2

import models.calendar.medicine
from models.user import User

template_loader = jinja2.FileSystemLoader(searchpath=".")
template_env = jinja2.Environment(loader=template_loader)


class BMI:
    @staticmethod
    def normalize(number, range_min, range_max):
        return (number - range_min) / (range_max - range_min)

    @staticmethod
    def calculate_bmi(weight, height):
        height = height / 100  # Convert height from cm to m
        return weight / (height**2)

    @staticmethod
    def get_bmi_data(bmi, age):
        # BMI ranges by age according to the World Health Organization (WHO)
        # The groups are ["Very low weight", "Low weight", "Healthy weight", "Overweight", "Obese"]
        BMI_ranges = {
            (0, 5): [
                (0, 14),
                (14, 16),
                (16, 18),
                (18, 20),
                (20, float("inf")),
            ],  # 0 to 5 years
            (6, 18): [
                (0, 15),
                (15, 17),
                (17, 19),
                (19, 22),
                (22, float("inf")),
            ],  # 6 to 18 years
            (19, 59): [
                (0, 16),
                (16, 18.5),
                (18.5, 25),
                (25, 30),
                (30, float("inf")),
            ],  # 19 to 59 years
            (60, float("inf")): [
                (0, 21),
                (21, 23),
                (23, 27),
                (27, 32),
                (32, float("inf")),
            ],  # 60 years or older
        }

        # Check the age range and get the corresponding BMI limits
        for age_range, BMI_ranges_age in BMI_ranges.items():
            age_min, age_max = age_range
            if age_min <= age <= age_max:
                for i, BMI_range in enumerate(BMI_ranges_age):
                    BMI_min, BMI_max = BMI_range
                    if BMI_min <= bmi < BMI_max:
                        return i, BMI.normalize(bmi, BMI_min, BMI_max)

    @staticmethod
    def normalized_bmi_to_range(bmi_group_index, bmi_normalized):
        if bmi_group_index == 0:
            return -36
        elif bmi_group_index == 4:
            return 36
        elif bmi_group_index == 1:
            return ((-17) - (-36)) * bmi_normalized + (-36)
        elif bmi_group_index == 2:
            return (17 - (-17)) * bmi_normalized + (-17)
        elif bmi_group_index == 3:
            return (36 - 17) * bmi_normalized + 17

    @staticmethod
    def get_html_group_names(bmi, group_index):
        bmi = round(bmi, 1)
        groups = {
            0: {
                "value": f"<span style='color: #516EB4; font-weight: bold'>Muy bajo peso "
                f"<span style='color: darkred'>({bmi})</span></span>",
                "order": 0,
            },
            1: {
                "value": f"<span style='color: #516EB4; font-weight: bold'>Bajo peso "
                f"<span style='color: #374A79FF'>({bmi})</span></span>",
                "order": 0,
            },
            2: {
                "value": f"<span style='color: #516EB4; font-weight: bold'>Peso saludable "
                f"<span style='color: #374A79FF'>({bmi})</span></span>",
                "order": 1,
            },
            3: {
                "value": f"<span style='color: #516EB4; font-weight: bold'>Sobrepeso "
                f"<span style='color: #374A79FF'>({bmi})</span></span>",
                "order": 2,
            },
            4: {
                "value": f"<span style='color: #516EB4; font-weight: bold'>Obesidad "
                f"<span style='color: darkred'>({bmi})</span></span>",
                "order": 2,
            },
        }
        base_groups = ["Bajo peso", "Peso saludable", "Sobrepeso"]
        base_groups[groups[group_index]["order"]] = groups[group_index]["value"]
        html_groups = base_groups
        return html_groups

    @staticmethod
    def get_bmi_html_percentage_and_groups(weight, height, age):
        bmi_index = BMI.calculate_bmi(weight, height)
        bmi_group_index, bmi_normalized = BMI.get_bmi_data(bmi_index, age)
        return BMI.normalized_bmi_to_range(
            bmi_group_index, bmi_normalized
        ), BMI.get_html_group_names(bmi_index, bmi_group_index)


def generate_base_file(data):
    template = template_env.get_template(
        "routers/export/pdf_generator/assets/index.html"
    )
    if (
        str(data["weight"]).replace(".", "", 1).isdigit()
        and str(data["height"]).replace(".", "", 1).isdigit()
        and str(data["age"]).replace(".", "", 1).isdigit()
    ):
        data["bmi"], data["groups"] = BMI.get_bmi_html_percentage_and_groups(
            data["weight"], data["height"], data["age"]
        )
    else:
        data["bmi"], data["groups"] = 0, [
            "Bajo peso",
            "<span style='color: #516EB4; font-weight: bold'>Peso saludable</span>",
            "Sobrepeso",
        ]
    template_string = template.render(**data)
    options = {
        "page-size": "A4",
        "margin-bottom": "30mm",
        "margin-top": "3mm",
        "margin-left": "3mm",
        "enable-local-file-access": "",
    }
    return pdfkit.from_string(
        template_string,
        css="routers/export/pdf_generator/assets/styles.css",
        options=options,
    )


def generate_footer_list(pages):
    def get_image_logo():
        with open("routers/export/pdf_generator/assets/logo.png", "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    data = {
        "image": get_image_logo,
        "pages": pages,
    }
    template = template_env.get_template(
        "routers/export/pdf_generator/assets/footer.html"
    )
    template_string = template.render(**data)
    options = {"page-size": "A4", "enable-local-file-access": ""}
    return pdfkit.from_string(
        template_string,
        css="routers/export/pdf_generator/assets/styles.css",
        options=options,
    )


def add_footer(base_file):
    base = PyPDF2.PdfReader(io.BytesIO(base_file))
    footer = PyPDF2.PdfReader(io.BytesIO(generate_footer_list(len(base.pages))))
    result = PyPDF2.PdfWriter()

    for page in range(len(base.pages)):
        page_base = base.pages[page]
        page_footer = footer.pages[page]
        page_footer.merge_page(page_base)
        result.add_page(page_footer)

    return result


def get_user_data(user: User):
    medicine_objects, _ = user.get_active_medicines_with_consumptions()
    medicines = []
    for medicine_object in medicine_objects:
        medicine_object: models.calendar.medicine.Medicine
        possible_days = ["L", "M", "M", "J", "V", "S", "D"]
        if medicine_object.days:
            days = [
                {
                    "day": possible_days[i],
                    "enabled": True if (i + 1) in medicine_object.days else False,
                }
                for i in range(len(possible_days))
            ]
        else:
            days = None
        if medicine_object.end_date:
            total_days = (medicine_object.end_date - medicine_object.start_date).days
            to_now_days = (datetime.datetime.now() - medicine_object.start_date).days
            percentage = max(1, int((to_now_days * 100) / total_days))

        medicines.append(
            {
                "name": medicine_object.name,
                "instructions": medicine_object.instructions,
                "presentation": medicine_object.presentation,
                "dosis_unit": medicine_object.dosis_unit,
                "dosis": medicine_object.dosis,
                "hours": medicine_object.hours,
                "days": days,
                "interval": medicine_object.interval,
                "percentage": percentage if medicine_object.end_date else None,
            }
        )
    measurements = [
        {
            "date": measurement.date,
            "type": measurement.type,
            "result": f"{measurement.value} {measurement.unit}",
        }
        for measurement in user.get_measurements(
            start=datetime.datetime.now() - datetime.timedelta(days=30)
        )
    ]
    last_month_predictions_by_symptom = len(
        [
            True
            for prediction in user.predictions_by_symptoms
            if prediction.date > datetime.datetime.now() - datetime.timedelta(days=30)
        ]
    )
    last_month_predictions_by_image = len(
        [
            True
            for prediction in user.predictions_by_image
            if prediction.date > datetime.datetime.now() - datetime.timedelta(days=30)
        ]
    )
    return {
        "name": user.get_fullname(),
        "weight": user.weight if user.weight else "N/A",
        "height": user.height if user.height else "N/A",
        "age": user.get_age() if user.birth else "N/A",
        "text_age": user.get_birth_text() if user.birth else "No hay información",
        "last_month_predictions": last_month_predictions_by_symptom
        + last_month_predictions_by_image,
        "medicines": medicines,
        "measurements": measurements,
        "supervisors": len(user.supervisors_list),
    }


def generate_pdf(user: User):
    base_file = generate_base_file(get_user_data(user))
    return add_footer(base_file)
