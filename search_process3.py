# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 11:09:36 2022

@author: Januario Cipriano
"""

import re
import os
import time
import json
import logging
import numpy as np
import pandas as pd
from glob import glob
from enum import Enum
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

# local modules
from instantiate_driver import initiate_driver
from classify_proposal import ClassifyProposal
    
def launch_driver():
    URL = 'http://10.245.87.77/itcore.sites/ITCore.Ui.Web/ITCore.aspx'
    driver = initiate_driver()
    driver.get(URL)
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver

def get_row(path_id):
    client_data = {}
    common_idenifier = '//*[@id="ContentPlaceHolder1_flwForm_egvSearchResult'
    identifiers = ['lbResultProcessNumber', 'lbResultTipo', 'lbResultClientName', 'lbResultUser', 
                   'lbResultCurrentCostCenter', 'lbResultCurrentUser', 'lbResultCreationDate',
                   'lbResultStatus']
    for identifier in identifiers:
        path = f'{common_idenifier}_{identifier}_{path_id}"]'
        path = driver.find_element(By.XPATH, path)
        col_name = identifier.split('lbResult')[1]
        client_data[col_name] = path.text
        
    client_no = driver.find_element(By.XPATH, f'{common_idenifier}"]/tbody/tr[2]/td[4]')
    client_data['client_no'] = client_no.text
    
    print(client_data)
    return client_data


def classify_proposal(row):
    if row != 'Crédito ao Consumo':
        return 'CVU Central'
    else:
        return 'Not Defined'
    
class Classify(Enum):
    FIRST = 'NWOW'
    SECOND = 'CVU Central'


def set_exceptional_companies(df, process_number):
    if (df.loc[process_number, 'Entidade Patronal'] == 'MLT' or
        df.loc[process_number, 'Entidade Patronal'] == 'CEDSIF'):
        df.loc[process_number, 'Area de Verificacao'] = Classify.SECOND.value

def update_excel_file(df, process_number, data):
    df.set_index('Nº', inplace=True)
    df.loc[process_number, 'Valor Requisitado'] = data.get('Valor_Requisitado')
    df.loc[process_number, 'Entidade Patronal'] = data.get('Entidade-Patronal')
    df.loc[process_number, 'ModificadoEm'] = datetime.now()
    
    if df.loc[process_number, 'Valor Requisitado'] > 500000:
        df.loc[process_number, 'Area de Verificacao'] = Classify.SECOND.value
    elif df.loc[process_number, 'Valor Requisitado'] == 0:
        pass
    elif df.loc[process_number, 'Valor Requisitado'] <= 500000:
        df.loc[process_number, 'Area de Verificacao'] = Classify.FIRST.value
    
    set_exceptional_companies(df, process_number)
    
    df.loc[process_number, 'IsUpdated'] = True
    df.reset_index(inplace=True)
    files = glob('*.xlsx')
    df.to_excel(os.getcwd() + "/" + files[-1], index=False)  
    
    
def check_if_is_updated(df, process_number):
    df.set_index('Nº', inplace=True)
    print(f"IsUpdated = {df.loc[process_number, 'IsUpdated']}")
    if not df.loc[process_number, 'IsUpdated']:
        df.reset_index(inplace=True)
        return True
    df.reset_index(inplace=True)
    return False

".\A200795"

def update_dataframe(process_number, collborador):
    files = glob('*.xlsx')
    df = pd.read_excel(files[0])
    df.set_index('Nº', inplace=True)
    print('ATTEMPTING TO UPDATE DATAFRAME')
    try:
        df.loc[process_number, 'Colaborador'] = collborador
        print('COLLABORATOR NAME Successfully UPDATED')
        df.loc[process_number, 'IsPropostaActualizada'] = False
        print('IsPropostaActualizada Successfully UPDATED')
    except Exception as e:
        print(e)
    df.reset_index(inplace=True)
    df.to_excel(files[0], index=False)
    print(f'Successfully updated PROCESS NUMBER {process_number}')

def search_client_process(process_number):
    # driver = launch_driver()
    # classify = ClassifyProposal()
    # driver.switch_to.parent_frame()

    # number_of_iterations = len(process_numbers)
    # print(f'PROCESS NUMBERS = {process_numbers}')
    # print(f'FUNCTION CALL - ITERATION {index}')
    
    # time_tracker = []

    # process_number = process_numbers[i]   # 1154192
    print(f'CURRENT PROCESS NUMBER = {process_number}')
    logging.warning(f'Handling PROCESS NUMBER {process_number}')

    # if check_if_is_updated(df, process_number):

    # print(f'================== ITERATION {i} ==================')
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="contentContainer_TMenus_rpCustMenu_LkCustMenu_3"]/div')))
    
    print('LOCATING MENU')
    time.sleep(3)
    menu = driver.find_element(By.XPATH, '//*[@id="contentContainer_TMenus_rpCustMenu_LkCustMenu_3"]/div')
    hidden_submenu = driver.find_element(By.XPATH, '//*[@id="contentContainer_TMenus_rpCustMenu_rpSubCustMenu_3_rpSubCustMenuChilds_0_LkSubMenuChild_0"]')
      
    actions = ActionChains(driver)
    actions.move_to_element(menu)
    actions.click(hidden_submenu)
    actions.perform()
    time.sleep(1.5)
    logging.warning('Successfully clicked on search href.')

    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "MainIframe")))
    driver.switch_to.frame(driver.find_element(By.ID, "MainIframe"))

    try:
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_ntbcProcessNumber_txField"]')))
        search_process_field_XPATH = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_ntbcProcessNumber_txField"]')
        search_process_field_XPATH.send_keys(str(process_number))
        time.sleep(0.5)
        logging.warning('Successfully inserted PROCESS NUMBER into input field')
        
        search_button_XPATH = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_fcontrols_btnSearch"]/span[2]')
        search_button_XPATH.click()
        logging.warning('Successfully clicked on Search button')
        # time.sleep(8)

        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '/html/body/form/div[3]/section/div/div[1]/div[2]/div[3]/div[1]/table/tbody/tr[2]')))

        try:
            print('CLICKING CLIEND_TD')
            client_td = driver.find_element(By.XPATH, '/html/body/form/div[3]/section/div/div[1]/div[2]/div[3]/div[1]/table/tbody/tr[2]')
            client_td.click()
            print('CLIEND_TD CLICKED')
            time.sleep(8)

            workflow_path = '/html/body/form/div[3]/section/span[2]/div[1]/div[2]/ul[2]/li[24]/span[1]'
            WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH, workflow_path)))

            try:
                workflow = driver.find_element(By.XPATH, workflow_path)
                print(workflow.text)
                print('CLICKING WORKFLOW')
                workflow.click()
                time.sleep(2)
                print('WORKFLOW ALREADY VISIBLE')

                # WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '/html/body/form/div[3]/section/span[2]/div[1]/div[1]/div/div[3]/ul/li[3]/a')))
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'PRÓXIMA ACÇÃO')]")))
                print('PROXIMA ACCAO ALREADY VISIBLE')
                print('WAITING FOR PROXIMA ACCAO TO BE CLICKABLE') 

                # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/section/span[2]/div[1]/div[1]/div/div[3]/ul/li[3]')))
                # print('CLICKED ON PROXIMA ACCAO')

                try:
                    print('LOCATING PROXIMA ACCAO')
                    # proxima_accao = driver.find_element(By.XPATH, '/html/body/form/div[3]/section/span[2]/div[1]/div[1]/div/div[3]/ul/li[3]/a')
                    proxima_accao = driver.find_element(By.XPATH, "//*[contains(text(),'PRÓXIMA ACÇÃO')]")
                    print('PROXIMA ACCAO LOCATED Successfully')
                    print(proxima_accao.location)
                    if proxima_accao.text == 'PRÓXIMA ACÇÃO':
                        print('THE TEXT MATCHES')
                        print('WAITING FOR PROXIMA ACCAO TO BE CLICKABLE')
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'PRÓXIMA ACÇÃO')]")))
                        print('ELEMENT CAN BE CLICKED')
                        proxima_accao.click()

                    # wait = WebDriverWait(driver, 10)
                    # element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/section/span[2]/div[1]/div[1]/div/div[3]/ul/li[3]/a')))
                    
                    # wait = WebDriverWait(driver, 10)
                    # element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/section/span[2]/div[1]/div[1]/div/div[3]/ul/li[3]')))
                    # print('WAITING 2 SECONDS TO CLICK ON PROXIMA ACCAO')
                    # time.sleep(8)
                    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/section/span[2]/div[1]/div[1]/div/div[3]/ul/li[3]'))).click()
                    # proxima_accao.click()
                    # # except Exception as e:
                    # #     print(e)
                    # print('PROXIMA ACCAO CLICKED')
                    # time.sleep(2)
                    # logging.warning(f'Successfully clicked on CLIENT result')

                    # collaborador1_path1 = '/html/body/form/div[3]/section/span[2]/div[1]/div[1]/div/div[3]/div[3]/div[1]/div[1]/div[7]/div[1]/table/tbody/tr/td/div/table/tbody/tr[2]/td[1]/span'
                    # collaborador2_path2 = '/html/body/form/div[3]/section/span[2]/div[1]/div[1]/div/div[3]/div[3]/div[1]/div[1]/div[7]/div[1]/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/span'
                    # estado1_path1 = '/html/body/form/div[3]/section/span[2]/div[1]/div[1]/div/div[3]/div[3]/div[1]/div[1]/div[7]/div[1]/table/tbody/tr/td/div/table/tbody/tr[2]/td[3]/span'
                    # estado2_path2 = '/html/body/form/div[3]/section/span[2]/div[1]/div[1]/div/div[3]/div[3]/div[1]/div[1]/div[7]/div[1]/table/tbody/tr/td/div/table/tbody/tr[3]/td[3]/span'

                    # collaborador1_path1 = driver.find_element(By.XPATH, collaborador1_path1)
                    # estado1_path1 = driver.find_element(By.XPATH, estado1_path1)
                    # print(f'collaborador1_path1 = {collaborador1_path1.text}.\t estado1_path1 = {estado1_path1.text}')

                    # collaborador2_path2 = driver.find_element(By.XPATH, collaborador2_path2)
                    # estado2_path2 = driver.find_element(By.XPATH, estado2_path2)
                    # print(f'collaborador2_path2 = {collaborador2_path2.text}.\t estado2_path2 = {estado2_path2.text}')

                    # if estado1_path1.text == 'Proposta Atualizada':
                    #     update_dataframe(process_number, collaborador1_path1.text)
                    # elif estado2_path2.text == 'Proposta Atualizada':
                    #     update_dataframe(process_number, collaborador2_path2.text)

                    # if estado1_path1.text == 'Submetida':
                    #     update_dataframe(process_number, collaborador1_path1.text)
                    # elif estado2_path2.text == 'Submetida':
                    #     update_dataframe(process_number, collaborador2_path2.text)

                    # time.sleep(2.5)
                    # driver.refresh()
                    # time.sleep(8)
                except Exception as e:
                    print('EXCEPTION ON PROXIMA ACCAO')
                    print(e)
                    # time.sleep(0.5)
                    # driver.refresh()
                    # time.sleep(8)
            except Exception as e:
                print('EXCEPTION ON WORKFLOW')
                print(e)
                # time.sleep(0.5)
                # driver.refresh()
                # time.sleep(8)
        except Exception as e:
            print('EXCEPTION ON CLIEND_TD')
            print(e)
            # time.sleep(0.5)
            # driver.refresh()
            # time.sleep(8)
    except Exception as e:
        print('EXCEPTION ON SEARCH BUTTON')
        print(e)
            # time.sleep(0.5)
            # driver.refresh()
            # time.sleep(8)

        # time.sleep(0.5)
        # driver.refresh()
        # time.sleep(8)


".\A200795"

def get_process_numbers():
    files = glob('*.xlsx')
    df = pd.read_excel(files[0])
    process_numbers = df[
        (df['Estado'] == 'Proposta Atualizada') &
        (df['IsPropostaActualizada'] == True)
    ]['Nº'].tolist()
    return process_numbers

def main():
    # df = pd.read_excel('Processos-22-Dec-2022 105957.xlsx')
    # process_numbers = df[
    #     (df['Estado'] == 'Proposta Atualizada') &
    #     (df['IsPropostaActualizada'] == True)
    # ]['Nº'].tolist()
    process_numbers = get_process_numbers()
    # driver = launch_driver()
    
    index = 0
    LOOK_CHECKER = False
    while len(process_numbers) > 0:
        print('=' * 50)
        print(process_numbers)
        print('=' * 50)

        if len(process_numbers) == 1:
            search_client_process(process_numbers[0])
            time.sleep(3)
            driver.close()
            break

        try:
            search_client_process(process_numbers[index])
            index += 1
        except Exception as e:
            index = 0
            print(e)
            # driver.close()

        time.sleep(2)
        driver.refresh()
        time.sleep(8)

        process_numbers = get_process_numbers()
        print('\n')
        print(f'REMAINING PROCESSES = {process_numbers}')
        print('\n')
        


".\A200795"

# if __name__=='__main__':
#     # count = 3
    
#     driver = launch_driver()
#     main()
#     # while count > 0:
#     #     main()
#     #     count -= 1














