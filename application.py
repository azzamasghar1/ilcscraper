from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
import time
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

directory = os.getcwd()
if os.name == 'posix':
    chromeDriver = directory + '/chromedriver'
else:
    chromeDriver = directory + '/chromedriver.exe'
option = webdriver.ChromeOptions()

directory = os.getcwd()
option.add_argument("--headless")
option.add_argument("window-size=1920,1080")
driver = webdriver.Chrome(executable_path=chromeDriver, options=option)
#driver.maximize_window()

@app.route('/login/<login>/<password>')
def login(login, password):
    # -------------------------------------------------------------------

    url = 'https://ebiz.licindia.in/AgentPortal/#Login'

    driver.get(url)
    driver.refresh()
    count = 0
    try:
        user_code = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'da_textfield-1100-inputEl')))
        user_code.clear()
        user_code.send_keys(login)
        count += 1
    except Exception as e:
        print(e)
        pass
    try:
        login_pass = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'da_textfield-1101-inputEl')))
        login_pass.clear()
        login_pass.send_keys(password)
        count += 1
    except Exception as e:
        print(e)
        pass
    try:
        login_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'da_button-1105')))
        login_button.click()
        count += 1
    except Exception as e:
        print(e)
        pass
    if count == 3:
        return jsonify({'status': 'success'})

    else:
        return jsonify({'status': 'failed'})


@app.route('/otp/<code>')
def otp(code):
    count = 0
    try:
        otp = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'da_textfield-1110-inputEl')))
        otp.send_keys(code)
        count += 1
    except Exception as e:
        print('otp')
        print(e)
    try:
        button_form = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'da_button-1117')))
        button_form.click()
        count += 1
    except Exception as e:
        print('button form')
        print(e)
        pass
    try:
        agent_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'da_widgetButton-1124')))
        agent_button.click()
        count += 1
    except Exception as e:
        print('agent button')
        print(e)
        pass
    if count == 3:
        return jsonify({'status': 'success'})

    else:
        return jsonify({'status': 'failed'})


@app.route('/commercedate/<fromDate>/<toDate>')
def commerceData(fromDate, toDate):
    tmp_from_date = fromDate.split('-')
    fromDate = '/'.join(tmp_from_date)

    tmp_to_date = toDate.split('-')
    toDate = '/'.join(tmp_to_date)
    print(fromDate, toDate)
    count = 0
    url = 'https://ebiz.licindia.in/AgentPortal/#AgentLanding'

    driver.get(url)
    print(driver.current_url)
    try:
        picker = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'da_combo-1152-inputEl')))  # da_combo-1415-trigger-picker
        picker.click()
        count += 1
    except Exception as e:
        print('mobile')
        print(e)
    try:
        commerce_date = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Commencement Date')]")))  # ext-element-178
        commerce_date.click()
        count += 1
    except Exception as e:
        print('commerce date')
        print(e)
        pass
    try:
        from_date = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'da_datefield-1161-inputEl')))  # da_datefield-1077-inputEl
        from_date.send_keys(fromDate)
        count += 1
    except Exception as e:
        print('from_date')
        print(e)
        pass
    try:
        to_date = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'da_datefield-1162-inputEl')))
        to_date.send_keys(toDate)
        count += 1
    except Exception as e:
        print('to_date')
        print(e)
        pass
    try:
        search = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'da_button-1170-btnIconEl')))  # da_button-1086-btnIconEl
        search.click()
        count += 1
    except Exception as e:
        print('search')
        print(e)
        pass
    try:
        time.sleep(5)
        totalPages = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div/div/div['
                                                      '1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div['
                                                      '2]/div/div/div/div/div/div/div[2]/div/div/div/div['
                                                      '3]/div/div/div[4]')))  # tbtext-1662 1693
        total_pages = totalPages.text
        total_pages = int(total_pages.replace('of ', ''))
        print(total_pages)
        count += 1
    except Exception as e:
        print('total pages')
        print(e)
        pass
    try:
        client_information = []
        SI_Number_list = []
        Policy_Number_list = []
        Customer_number_list = []
        Doc_list = []
        Premium_list = []
        Mode_list = []
        FUP_list = []
        Agent_Code_list = []
        Plan_list = []
        Term_list = []
        Sum_Assured_list = []
        Status_list = []
        # just to see if all element are on screen
        SI_Number = str(
            '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/table[1]/tbody/tr/td[1]/div')
        _SI_Number = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, SI_Number)))
        for page in range(0, total_pages):
            for row in range(1, 11):
                try:
                    SI_Number = str(
                        '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/table[' + str(
                            row) + ']/tbody/tr/td[1]/div')
                    _SI_Number = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, SI_Number)))
                    SI_Number_list.append(_SI_Number.text)
                except Exception as e:
                    print(e)
                    pass
            for row in range(1, 11):
                try:
                    Policy_Number = str(
                        '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/table[' + str(
                            row) + ']/tbody/tr/td[2]/div')
                    _Policy_Number = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, Policy_Number)))
                    Policy_Number_list.append(_Policy_Number.text)
                except Exception as e:
                    print(e)
                    pass
            for row in range(1, 11):
                try:
                    Customer_number = str(
                        '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/table[' + str(
                            row) + ']/tbody/tr/td[3]/div')
                    _Customer_number = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, Customer_number)))
                    Customer_number_list.append(_Customer_number.text)
                except Exception as e:
                    print(e)
                    pass
            for row in range(1, 11):
                try:
                    Doc = str(
                        '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/table[' + str(
                            row) + ']/tbody/tr/td[4]/div')
                    _Doc = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, Doc)))
                    Doc_list.append(_Doc.text)
                except Exception as e:
                    print(e)
                    pass
            for row in range(1, 11):
                try:
                    Premium = str(
                        '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/table[' + str(
                            row) + ']/tbody/tr/td[5]/div')
                    _Premium = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, Premium)))
                    _tmp = _Premium.text
                    _tmp = _tmp.replace('₹', '')
                    Premium_list.append(_tmp)
                except Exception as e:
                    print(e)
                    pass
            for row in range(1, 11):
                try:
                    Mode = str(
                        '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/table[' + str(
                            row) + ']/tbody/tr/td[6]/div')
                    _Mode = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, Mode)))
                    Mode_list.append(_Mode.text)
                except Exception as e:
                    print(e)
                    pass
            for row in range(1, 11):
                try:
                    FUP = str(
                        '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/table[' + str(
                            row) + ']/tbody/tr/td[7]/div')
                    _FUP = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, FUP)))
                    FUP_list.append(_FUP.text)
                except Exception as e:
                    print(e)
                    pass
            for row in range(1, 11):
                try:
                    Agent_Code = str(
                        '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/table[' + str(
                            row) + ']/tbody/tr/td[8]/div')
                    _Agent_Code = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, Agent_Code)))
                    Agent_Code_list.append(_Agent_Code.text)
                except Exception as e:
                    print(e)
                    pass
            for row in range(1, 11):
                try:
                    Plan = str(
                        '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/table[' + str(
                            row) + ']/tbody/tr/td[9]/div')
                    _Plan = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, Plan)))
                    Plan_list.append(_Plan.text)
                except Exception as e:
                    print(e)
                    pass
            for row in range(1, 11):
                try:
                    Term = str(
                        '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/table[' + str(
                            row) + ']/tbody/tr/td[10]/div')
                    _Term = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, Term)))
                    Term_list.append(_Term.text)
                except Exception as e:
                    print(e)
                    pass
            for row in range(1, 11):
                try:
                    Sum_Assured = str(
                        '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/table[' + str(
                            row) + ']/tbody/tr/td[11]/div')
                    _Sum_Assured = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, Sum_Assured)))
                    _tmp = _Sum_Assured.text
                    _tmp = _tmp.replace('₹', '')
                    Sum_Assured_list.append(_tmp)
                except Exception as e:
                    print(e)
                    pass
            for row in range(1, 11):
                try:
                    Status = str(
                        '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/table[' + str(
                            row) + ']/tbody/tr/td[12]/div')
                    _Status = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, Status)))
                    Status_list.append(_Status.text)
                except Exception as e:
                    print(e)
                    pass

            next_button = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.ID, 'button-1432')))
            next_button.click()
            time.sleep(2)
            count += 1

    except Exception as e:
        print(e)
        pass
    client_information.append({
        'si#': Status_list,
        'policy number': Policy_Number_list,
        'customer name': Customer_number_list,
        'doc': Doc_list,
        'premium': Premium_list,
        'mode': Mode_list,
        'fup': FUP_list,
        'agent code': Agent_Code_list,
        'plan': Plan_list,
        'term': Term_list,
        'sum assured': Sum_Assured_list,
        'status': Status_list
    })
    print(count)
    print(client_information)
    if count >= 7:

        return jsonify({'status': 'success', 'data': client_information})

    else:
        return jsonify({'status': 'failed'})

