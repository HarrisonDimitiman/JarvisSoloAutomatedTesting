class LoginXpath:
    username = '/html/body/div/div/div/div/div[1]/div/form/div[1]/div/input'
    password = '/html/body/div/div/div/div/div[1]/div/form/div[2]/div[2]/input'
    login_btn = '/html/body/div/div/div/div/div[1]/div/form/button'
    main_header = '/html/body/div[1]/main/header'
    login_error = '/html/body/div/div/div/div/div[1]/div/form/p'
    logo_xpath = '/html/body/div/div/div/div/div[1]/div/div/a/img'
    no_vpn = '/html/body/div/div/div[1]'


class CalendarDateRangeXpath:
    # --Calendar Date Range
    date_picker = '//*[@class="vue-daterange-picker"]'
    curr_monthfrom = "/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/table/thead/tr/th[2]"
    curr_yearfrom = "/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/table/thead/tr/th[2]/div/input"
    curr_monthto = "/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div/table/thead/tr/th[2]/div/select"
    curr_yearto = "/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div/table/thead/tr/th[2]/div/input"
