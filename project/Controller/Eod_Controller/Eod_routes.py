from crypt import methods
from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from Project.Controller.Global_Controller.Global_test import Login
from .Eod_xpath import EodXpath, BreakdownXpath, EodSetupXpath, ModalMetricXpath, ModalCloseBtnXpath
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re

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
            
            result[metric] = {
                "main": None,
                "breakdown": "0"
            }

            # Get main view metric value
            xpaths[metric]["main"].findElement(driver)
            result[metric]["main"] = xpaths[metric]["main"].getValue()

            # Open breakdown modal
            xpaths[metric]["breakdown"]["open_modal"].findElement(driver)
            xpaths[metric]["breakdown"]["open_modal"].click(driver)

            # Get modal metric value
            xpaths[metric]["breakdown"]["metric"].findElement(driver)

            if xpaths[metric]["breakdown"]["metric"].element != None and xpaths[metric]["breakdown"]["metric"].instantiated:
                temp = xpaths[metric]["breakdown"]["metric"].getValue()

                if xpaths[metric]["breakdown"]["metric"].type == 'collection' and temp == 1 and "Nothing to show" in xpaths[metric]["breakdown"]["metric"].element[0].text:
                    result[metric]['breakdown'] = "0"

            # Close breakdown modal
            xpaths[metric]["breakdown"]["close_modal"].findElement(driver)
            xpaths[metric]["breakdown"]["close_modal"].click(driver)

        print(result)
        result = cleanValues(result)
        print(result)
        
    except Exception as e:
        print(f"Some error in here {e}")
    finally:
        driver.quit()
        return result

def getXpath():
    return {
        "collection": getMainBreakdown(EodXpath.collection, BreakdownXpath.collection, ModalMetricXpath.collection, ModalCloseBtnXpath.collection),
        "adjustments": getMainBreakdown(EodXpath.adjustments, BreakdownXpath.adjustments, ModalMetricXpath.adjustments, ModalCloseBtnXpath.adjustments),
        "case_acceptance": getMainBreakdown(EodXpath.case_acceptance, BreakdownXpath.case_acceptance, ModalMetricXpath.case_acceptance, ModalCloseBtnXpath.case_acceptance),
        "missing_ref": getMainBreakdown(EodXpath.missing_ref, BreakdownXpath.missing_ref, ModalMetricXpath.missing_ref, ModalCloseBtnXpath.missing_ref),
        "no_show": getMainBreakdown(EodXpath.no_show, BreakdownXpath.no_show, ModalMetricXpath.no_show, ModalCloseBtnXpath.no_show),
        "daily_coll": getMainBreakdown(EodXpath.daily_coll, BreakdownXpath.daily_coll, ModalMetricXpath.daily_coll, ModalCloseBtnXpath.daily_coll),
        "hyg_reapp": getMainBreakdown(EodXpath.hyg_reapp, BreakdownXpath.hyg_reapp, ModalMetricXpath.hyg_reapp, ModalCloseBtnXpath.hyg_reapp),
        "new_patients": getMainBreakdown(EodXpath.new_patients, BreakdownXpath.new_patients, ModalMetricXpath.new_patients, ModalCloseBtnXpath.new_patients),
        "same_day_treat": getMainBreakdown(EodXpath.same_day_treat, BreakdownXpath.same_day_treat, ModalMetricXpath.same_day_treat, ModalCloseBtnXpath.same_day_treat),
        "pt_portion": getMainBreakdown(EodXpath.pt_portion, BreakdownXpath.pt_portion, ModalMetricXpath.pt_portion, ModalCloseBtnXpath.pt_portion)
    }

def getMainBreakdown(main, open_brkdn, breakdown, close_btn):
    return {
        "main": main,
        "breakdown": {
            "open_modal": open_brkdn,
            "metric": breakdown,
            "close_modal": close_btn
        }
    }

def cleanValues(dict):
    for metric in dict:
        dict[metric]['main'] = re.sub("[^0-9.]", "", dict[metric]['main'])
        dict[metric]['breakdown'] = re.sub("[^0-9.]", "", dict[metric]['breakdown'])
    
    return dict