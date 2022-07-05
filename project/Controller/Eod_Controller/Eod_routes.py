from crypt import methods
from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from Project.Controller.Global_Controller.Global_test import Login
from .Eod_xpath import EodXpath, BreakdownXpath, EodSetupXpath, ModalMetricXpath
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

eod = Blueprint('eod', __name__)

@eod.route("/eod-form", methods=["POST", "GET"])
def eodForm():
    if request.method == 'POST':
        print(request.form)

        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = {'browser': 'ERROR'}
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), desired_capabilities=d)
        Login.login(driver, "https://solo.next.jarvisanalytics.com/end-of-day", "testryan", "Jarvis.123")
        
        if not driver:
            return False

        testEod(driver)
    return render_template('Eod_Template/Eod_index.html')

def testEod(driver):
    result = {}

    try:
        date_picker = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, EodSetupXpath.date_picker))
        )

        xpaths = getXpath()

        for metric in xpaths:
            # print(xpaths[metric]["main"])

            result[metric] = {}
            # result[metric]["main"] = driver.find_element(
            #     by = By.XPATH,
            #     value = xpaths[metric]["main"]
            # ).get_attribute("value")
            xpaths[metric]["main"].instantiateElement(driver)

            result[metric]["main"] = xpaths[metric]["main"].getValue()

            # breakdown_btn = driver.find_element(
            #     by = By.XPATH,
            #     value = xpaths[metric]["breakdown"]["xpath"]
            # )
            # breakdown_btn.click()
            xpaths[metric]["breakdown"]["button"].instantiateElement(driver)
            xpaths[metric]["breakdown"]["button"].click()

            xpaths[metric]["breakdown"]["metric"].instantiateElement(driver)
            result[metric]["breakdown"] = xpaths[metric]["breakdown"]["metric"].getValue()

            # web_element = WebDriverWait(driver, 60).until(
            #     EC.presence_of_element_located((By.XPATH, ))
            # )
        print(result)


        
    except Exception as e:
        print(f"Some error in here {e}")
    finally:
        driver.quit()
        return result

def getXpath():
    return {
        "collection": getMainBreakdown(EodXpath.collection, BreakdownXpath.collection, ModalMetricXpath.collection),
        "adjustments": getMainBreakdown(EodXpath.adjustments, BreakdownXpath.adjustments, ModalMetricXpath.adjustments),
        "case_acceptance": getMainBreakdown(EodXpath.case_acceptance, BreakdownXpath.case_acceptance, ModalMetricXpath.case_acceptance),
        "missing_ref": getMainBreakdown(EodXpath.missing_ref, BreakdownXpath.missing_ref, ModalMetricXpath.missing_ref),
        "no_show": getMainBreakdown(EodXpath.no_show, BreakdownXpath.no_show, ModalMetricXpath.no_show),
        "daily_coll": getMainBreakdown(EodXpath.daily_coll, BreakdownXpath.daily_coll, ModalMetricXpath.daily_coll),
        "hyg_reapp": getMainBreakdown(EodXpath.hyg_reapp, BreakdownXpath.hyg_reapp, ModalMetricXpath.hyg_reapp),
        "new_patients": getMainBreakdown(EodXpath.new_patients, BreakdownXpath.new_patients, ModalMetricXpath.new_patients),
        "same_day_treat": getMainBreakdown(EodXpath.same_day_treat, BreakdownXpath.same_day_treat, ModalMetricXpath.same_day_treat),
        "pt_portion": getMainBreakdown(EodXpath.pt_portion, BreakdownXpath.pt_portion, ModalMetricXpath.pt_portion)
    }

def getMainBreakdown(main, button, breakdown):
    return {
        "main": main,
        "breakdown": {
            "button": button,
            "metric": breakdown
        }
    }


