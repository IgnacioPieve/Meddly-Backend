
import base64
import io

import jinja2
import pdfkit
import PyPDF2

template_loader = jinja2.FileSystemLoader(searchpath=".")
template_env = jinja2.Environment(loader=template_loader)


class BMI:
    @staticmethod
    def normalize(number, range_min, range_max):
        return (number - range_min) / (range_max - range_min)

    @staticmethod
    def calculate_bmi(weight, height):
        height = height / 100  # Convert height from cm to m
        return weight / (height ** 2)

    @staticmethod
    def get_bmi_data(bmi, age):
        # BMI ranges by age according to the World Health Organization (WHO)
        # The groups are ["Very low weight", "Low weight", "Healthy weight", "Overweight", "Obese"]
        BMI_ranges = {
            (0, 5): [(0, 14), (14, 16), (16, 18), (18, 20), (20, float('inf'))],  # 0 to 5 years
            (6, 18): [(0, 15), (15, 17), (17, 19), (19, 22), (22, float('inf'))],  # 6 to 18 years
            (19, 59): [(0, 16), (16, 18.5), (18.5, 25), (25, 30), (30, float('inf'))],  # 19 to 59 years
            (60, float('inf')): [(0, 21), (21, 23), (23, 27), (27, 32), (32, float('inf'))]  # 60 years or older
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
                "value": f"<span style='color: #516EB4; font-weight: bold'>Muy bajo peso <span style='color: darkred'>({bmi})</span></span>",
                "order": 0
            },
            1: {
                "value": f"<span style='color: #516EB4; font-weight: bold'>Bajo peso <span style='color: #374A79FF'>({bmi})</span></span>",
                "order": 0
            },
            2: {
                "value": f"<span style='color: #516EB4; font-weight: bold'>Peso saludable <span style='color: #374A79FF'>({bmi})</span></span>",
                "order": 1
            },
            3: {
                "value": f"<span style='color: #516EB4; font-weight: bold'>Sobrepeso <span style='color: #374A79FF'>({bmi})</span></span>",
                "order": 2
            },
            4: {
                "value": f"<span style='color: #516EB4; font-weight: bold'>Obesidad <span style='color: darkred'>({bmi})</span></span>",
                "order": 2
            }
        }
        base_groups = ["Bajo peso", "Peso saludable", "Sobrepeso"]
        base_groups[groups[group_index]["order"]] = groups[group_index]["value"]
        html_groups = base_groups
        return html_groups

    @staticmethod
    def get_bmi_html_percentage_and_groups(weight, height, age):
        bmi_index = BMI.calculate_bmi(weight, height)
        bmi_group_index, bmi_normalized = BMI.get_bmi_data(bmi_index, age)
        return BMI.normalized_bmi_to_range(bmi_group_index, bmi_normalized), BMI.get_html_group_names(bmi_index,
                                                                                              bmi_group_index)


def generate_base_file():
    template = template_env.get_template("index.html")
    data = {
        "name": "Ignacio Pieve Roiger",
        "weight": 90,
        "height": 170,
        "age": 23,
        "medicines": [
            {
                "name": "Paracetamol",
                "instructions": "Disolver la pastilla en agua",
                "presentation": "Pastilla",
                "dosis_unit": "mg",
                "dosis": 1.5,
                "hours": ["08:00", "11:30", "18:00"],
                "days": [
                    {"day": "L", "enabled": False},
                    {"day": "M", "enabled": True},
                    {"day": "M", "enabled": True},
                    {"day": "J", "enabled": False},
                    {"day": "V", "enabled": False},
                    {"day": "S", "enabled": True},
                    {"day": "D", "enabled": False},
                ],
                "percetage": "50%",
            },
        ],
        "measurements": [
            {
                "date": "2020-01-01",
                "type": "Glucosa",
                "result": '130 mg/dL'
            },
            {
                "date": "2020-01-01",
                "type": "Glucosa",
                "result": '130 mg/dL'
            },
            {
                "date": "2020-01-01",
                "type": "Glucosa",
                "result": '130 mg/dL'
            },
        ]
    }
    data['bmi'], data['groups'] = BMI.get_bmi_html_percentage_and_groups(data['weight'], data['height'], data['age'])
    template_string = template.render(**data)
    options = {
        'page-size': 'A4',
        'margin-bottom': '30mm',
        'margin-top': '3mm',
        'margin-left': '3mm',
        "enable-local-file-access": ""
    }
    return pdfkit.from_string(template_string, css='assets/styles.css', options=options)



def generate_footer_list(pages):
    def get_image_logo():
        with open('assets/logo.png', 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    data = {
        'image': get_image_logo,
        'pages': pages,
    }
    template = template_env.get_template("assets/footer.html")
    template_string = template.render(**data)
    options = {
        'page-size': 'A4',
        "enable-local-file-access": ""
    }
    return pdfkit.from_string(template_string, css='assets/styles.css', options=options)


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

