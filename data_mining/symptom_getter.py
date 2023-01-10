from selenium import webdriver
from selenium.webdriver.common.by import By


def get_symptoms():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/List_of_medical_symptoms")
    symptoms = driver.find_element(By.CLASS_NAME, 'https://en.wikipedia.org/wiki/List_of_medical_symptoms')
    print(len(symptoms))


if __name__ == '__main__':
    get_symptoms()
