from Project.Controller.Global_Controller.Global_test import Login

def testEod(testcode):
    # INSERT CODE FOR DECODING THE TESTCODE

    driver = Login.login("https://solo.next.jarvisanalytics.com/login")

    if not driver:
        return False

    try:
        pass
    except Exception as e:
        pass
    finally:
        driver.quit()