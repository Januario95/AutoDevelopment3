# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 11:57:12 2022

@author: Januario Cipriano
"""

import time
import shutil
import logging
import threading
import numpy as np
import pandas as pd
from glob import glob
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from multiprocessing import Process
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from instantiate_driver import initiate_driver
from data_structure import ADT, NodeStructure
from classify_proposal import ClassifyProposal


adt = ADT()

".\A200795"




def start_driver():
    URL = 'http://10.245.87.77/itcore.sites/ITCore.Ui.Web/ITCore.aspx'

    driver = initiate_driver()

    driver.get(URL)

    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "MainIframe")))
    driver.switch_to.frame(driver.find_element(By.ID, "MainIframe"))

    dept_processes = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_fwcInit_BtnDepartmentWorklist"]')
    dept_processes.click()
    time.sleep(10)
    return driver

driver = start_driver()

def handle_collaborator():
    data = []
    try:
        for index in range(2, 4):
            print('FETCHING COLLABORATOR')
            row = {}
            try:
                col_id = f'//*[@id="ctl00_ContentPlaceHolder1_ff1_fc1_tabs_procValidationControl_fic_ficComments_rptComments_ctl0{index}_lblColaborador"]'
                elem = driver.find_element(By.XPATH, col_id)
                row['Collaborador'] = elem.text

                col_id2 = f'//*[@id="ctl00_ContentPlaceHolder1_ff1_fc1_tabs_procValidationControl_fic_ficComments_rptComments_ctl0{index}_lblEstado"]'
                elem = driver.find_element(By.XPATH, col_id2)
                row['Estado'] = elem.text
            except Exception as e:
                print('ERROR FETCHING COLLABORATOR NAME')
            print(row)
            data.append(row)
    except Exception as e:
        print('ERROR DURING ITERATION')

    print(data)
    final = [val for val in data if val['Estado'] == 'Proposta Atualizada' or
                                val['Estado'] == 'Submetida']
    return final[0]


".\A200795"

def get_row(path_id):
    print(f'STARTING TO FETCH ROW {path_id}')

    row_data = {}
    common_idenifier = '//*[@id="ContentPlaceHolder1_flwForm_fwcInit_gridAbertConta'
    identifiers = ['lb_timer', 'lb_nProcesso', 'lb_tipoConta', 'lb_nome', 'span_Segmento',
                   'lb_estado', 'lb_branch', 'lb_user']
    
    for identifier in identifiers:
        path = f'{common_idenifier}_{identifier}_{path_id}"]'
        path = driver.find_element(By.XPATH, path)
        col_name = identifier.split('_')[1]
        row_data[col_name] = path.text
    
    R = driver.find_element(By.XPATH, f'{common_idenifier}"]/tbody/tr[{2+path_id}]/td[7]')
    row_data['R'] = R.text
    
    creation_date = driver.find_element(By.XPATH, f'{common_idenifier}"]/tbody/tr[{2+path_id}]/td[8]')
    row_data['CreationDate'] = creation_date.text
    row_data['ModificadoEm'] = datetime.now()
    row_data['ValorRequisitado'] = 0
    row_data['Colaborador2'] = 'CVU Central'
    row_data['EntidadePatronal'] = 'Nao Definida'
    row_data['IsUpdated'] = False
    row_data['IsPropostaActualizada'] = False

    print(f"PROCESS NUMBER = {row_data['nProcesso']} at ROW = {path_id}")    

    if row_data['estado'] == 'Proposta Atualizada':
        row_data['IsPropostaActualizada'] = True

    node = NodeStructure(**row_data)
    print(node.values['state'])

    print(node.values)
    print('\n')
    adt.push(node)


".\A200795"

def refresh_to_initial_page():
    print('REFRESHING PAGE...')
    driver.refresh()
    print('PAGE SUCCESSFULLY REFRESHED')
    time.sleep(8)

".\A200795"

# def fetch_updated_proposals():
#     refresh_to_initial_page()

#     classify = ClassifyProposal()
#     df = classify.dataframe
#     df_copy = classify.get_updated_proposals()
#     print(df.head())

#     process_numbers = df_copy['Nº'].values.tolist()

#     while process_numbers:
#         for process_number in process_numbers:
#             print(f'PROCESS NUMBER = {process_number}')
            
#             try:
#                 print('WAITING FOR ELEMENT TO BE VISIBLE')
#                 WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="contentContainer_TMenus_rpCustMenu_LkCustMenu_3"]/div')))

#                 menu = driver.find_element(By.XPATH, '//*[@id="contentContainer_TMenus_rpCustMenu_LkCustMenu_3"]/div')
#                 hidden_submenu = driver.find_element(By.XPATH, '//*[@id="contentContainer_TMenus_rpCustMenu_rpSubCustMenu_3_rpSubCustMenuChilds_0_LkSubMenuChild_0"]')
                  
#                 actions = ActionChains(driver)
#                 actions.move_to_element(menu)
#                 actions.click(hidden_submenu)
#                 actions.perform()
#                 time.sleep(1.5)
#                 logging.warning('Successfully clicked on search href.')
#             except Exception as e:
#                 print(e)

#             WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "MainIframe")))
#             driver.switch_to.frame(driver.find_element(By.ID, "MainIframe"))

#             try:
#                 WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_ntbcProcessNumber_txField"]')))
#                 search_process_field_XPATH = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_ntbcProcessNumber_txField"]')
#                 search_process_field_XPATH.send_keys(str(process_number))
#                 time.sleep(0.5)
#                 logging.warning('Successfully inserted PROCESS NUMBER into input field')
                
#                 search_button_XPATH = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_fcontrols_btnSearch"]/span[2]')
#                 search_button_XPATH.click()
#                 logging.warning('Successfully clicked on Search button')
#                 # time.sleep(30)

#                 try:
#                     WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_egvSearchResult"]/tbody/tr[2]')))
#                     client_td = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_egvSearchResult"]/tbody/tr[2]')
#                     client_td.click()
#                     time.sleep(1.5)
#                     logging.warning(f'Successfully clicked on CLIENT result')

#                     workflow_path = '//*[@id="st_16"]/span[1]'
#                     WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH, workflow_path)))
#                     workflow = driver.find_element(By.XPATH, workflow_path)
#                     print(workflow.text)
#                     print('CLICKING WORKFLOW')
#                     workflow.click()
#                     print('WORKFLOW CLICKED')
#                     time.sleep(8)

#                     next_action_path = '/html/body/form/div[3]/section/span[2]/div[1]/div[1]/div/div[3]/ul/li[3]/a'
#                     WebDriverWait(driver, 80).until(EC.visibility_of_element_located((By.XPATH, next_action_path)))
#                     next_action = driver.find_element(By.XPATH, next_action_path)
#                     WebDriverWait(driver, 80).until(EC.element_to_be_clickable((By.XPATH, next_action_path)))
#                     print(f'text = {next_action.text}')
#                     print('CREATING ACTION CHAINS')
#                     actions = ActionChains(driver)
#                     print('MOVING ELEMENT TO NEXT ACCAO')
#                     time.sleep(1.5)
#                     actions.move_to_element(next_action)
#                     time.sleep(1.5)
#                     print('ELEMENT MOVED TO NEXT ACCAO')
#                     actions.click(next_action)
#                     time.sleep(1.5)
#                     print('ATTEMPTING TO CLICK ON NEXT ACCAO')
#                     actions.perform()
#                     print('NEXT ACCAO CLICKED SUCCESSFULLY')
#                     # next_action.click()
#                     time.sleep(4)

#                     try:
#                         print('WAITING VISIBILITY OF ELEMENT')
#                         WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ff1_fc1_tabs_procValidationControl_fic_ficComments"]/div')))
#                         print('ELEMENT IS ALREADY VISIBILITY')

#                         estado1_path1 = '//*[@id="ctl00_ContentPlaceHolder1_ff1_fc1_tabs_procValidationControl_fic_ficComments_rptComments_ctl02_lblEstado"]'
#                         estado1_path1 = driver.find_element(By.XPATH, estado1_path1)
#                         print(f'ESTADO 1: {estado1_path1.text}')

#                         estado2_path2 = '//*[@id="ctl00_ContentPlaceHolder1_ff1_fc1_tabs_procValidationControl_fic_ficComments_rptComments_ctl03_lblEstado"]'
#                         estado2_path2 = driver.find_element(By.XPATH, estado2_path2)
#                         print(f'ESTADO 2: {estado2_path2.text}')

#                         collaborador1_path1 = '//*[@id="ctl00_ContentPlaceHolder1_ff1_fc1_tabs_procValidationControl_fic_ficComments_rptComments_ctl02_lblColaborador"]'
#                         collaborador1_path1 = driver.find_element(By.XPATH, collaborador1_path1)

#                         collaborador2_path2 = '//*[@id="ctl00_ContentPlaceHolder1_ff1_fc1_tabs_procValidationControl_fic_ficComments_rptComments_ctl03_lblColaborador"]'
#                         collaborador2_path2 = driver.find_element(By.XPATH, collaborador2_path2)                

#                         if estado1_path1.text == 'Proposta Atualizada':
#                             print(f'Collaborador: {collaborador1_path1.text}')
#                             classify.update_updated_proposals(process_number, collaborador1_path1.text)
#                         elif estado2_path2.text == 'Proposta Atualizada':
#                             print(f'Collaborador: {collaborador2_path2.text}')
#                             classify.update_updated_proposals(process_number, collaborador2_path2.text)

#                         if estado1_path1.text == 'Submetida':
#                             print(f'Collaborador: {collaborador1_path1.text}')
#                             classify.update_updated_proposals(process_number, collaborador1_path1.text)
#                         elif estado2_path2.text == 'Submetida':
#                             print(f'Collaborador: {collaborador2_path2.text}')
#                             classify.update_updated_proposals(process_number, collaborador2_path2.text)
#                     except Exception as e:
#                         print(e)

#                     time.sleep(8)
#                 except Exception as e:
#                     print(e)
#             except Exception as e:
#                 print(e)

#             df_copy = classify.get_updated_proposals()
#             process_numbers = df_copy['Nº'].values.tolist()
#             # refresh_to_initial_page()

".\A200795"

def fetch_table():
    logging.warning(f'Fetching page {adt.PAGE_COUNT}')
    adt.PAGE_COUNT += 1
    for path_id in range(0, 15):
        try:
            start = datetime.now().strftime('%d-%b-%Y %H:%M:%S')

            get_row(path_id)
            time.sleep(1)
            end = datetime.now().strftime('%d-%b-%Y %H:%M:%S')
            logging.warning(f'Fetching row {path_id+1}. \tStarted at {start}. \tEnded at: {end}')
            driver.save_screenshot('Page1.png')
        except Exception as exc:
            print(exc)
            logging.warning(exc)
    logging.warning('\n')
    time.sleep(3)
    print('\n')

def fetch_remaining_pages_2(page_id):
    link = driver.find_element(By.XPATH, f'//*[@id="ContentPlaceHolder1_flwForm_fwcInit_grvPager_repPager_pb1_{page_id}"]')
    link.click()


".\A200795"

        
def fetch_remaining_pages():
    link_ids = []
    for link_id in range(1, 30):
        try:
            link = driver.find_element(By.XPATH, f'//*[@id="ContentPlaceHolder1_flwForm_fwcInit_grvPager_repPager_pb1_{link_id}"]')
            link_ids.append(link_id)
        except Exception:
            pass

    for link_id in link_ids:
        print(f'\nFETCHING PAGE = {link_id}')
        try:
            link = driver.find_element(By.XPATH, f'//*[@id="ContentPlaceHolder1_flwForm_fwcInit_grvPager_repPager_pb1_{link_id}"]')
            link.click()
            time.sleep(8)
            fetch_table()
            # time.sleep(6)
            save_to_excel()
            time.sleep(2)
        except Exception as exc:
            print(exc)
            logging.warning(exc)
    

".\A200795"


def save_to_excel():
    df = pd.DataFrame(adt.data)
    df.columns = 'SLA, Nº, Tipo, Nome, Segmento, Estado, Balcão de Criação, Colaborador, R, Dt. Criação, DownloadedAt, Valor Requisitado, Area de Verificacao, Entidade Patronal, IsUpdated, IsPropostaActualizada'.split(', ')
    now = datetime.now()
    if now.hour < 12:
        now = now.date().strftime('%d.%m.%Y')
        filename = f'Fluxo - {now} (Manha).xlsx'
    else:
        now = now.date().strftime('%d.%m.%Y')
        filename = f'Fluxo - {now} (Tarde).xlsx'

    df.drop_duplicates('Nº', inplace=True)

    df.to_excel(filename, index=False)
    time.sleep(2)

".\A200795"


def move_older_files():
    files = glob('Logs/Fetch-Data/*.log')
    if len(files) > 0:
        path = Path(files[0])
        if path.exists():
            filename = path.name
            shutil.move(files[0], f'Logs/Fetch-Data/Old-Logs/{filename}')


def main():
    # move_older_files()

    # filename = datetime.now().strftime('%d-%b-%Y %H%M%S%z.log')
    # logging.basicConfig(filename=f'Logs/Fetch-Data/{filename}',
    #                     level=logging.WARNING,
    #                     format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')

    # logging.warning('Started to fetch data.')
    fetch_table()
    
    fetch_remaining_pages()
    
    save_to_excel()

    # fetch_updated_proposals()
    
    # driver.close()
    # time.sleep(2)


".\A200795"

def fetch_table_page(page_id):
    for td_id in range(0, 15):
        try:
            # driver = start_driver()
            link = driver.find_element(By.XPATH, f'//*[@id="ContentPlaceHolder1_flwForm_fwcInit_grvPager_repPager_pb1_{page_id}"]')
            print(f'LINK ID: {link.text}')
            link.click()
            time.sleep(7)

            get_row(td_id)
        except Exception as e:
            pass


def run_all():
    for i in range(6):
        t = threading.Thread(target=fetch_table_page, args =[i])
        t.start()


".\A200795"

if __name__=='__main__':
    start_time = time.perf_counter()
    main()

    # Re-fetch missed rows
    # from verify_remaining import fetch_remaining_rows, save_df_and_merge

    # print('STARTING TO FETCH REMAINING ROWS========================')
    # for i in range(3):
    #     fetch_remaining_rows(driver)
    #     time.sleep(2)

    #     print('MERGING AND SAVING FILES================================')
    #     save_df_and_merge()
    #     time.sleep(3)

    from search_process import search_client_process 

    print('SWITCHING TO PARENT NODE================================')
    driver.switch_to.parent_frame()
    print('STARGING TO SEARCH PROPOSALS============================')
    for i in range(4):
        search_client_process(driver)
        time.sleep(2)

    from split_proposal_types import split_proposal
    split_proposal()

    elapsed_time = time.perf_counter() - start_time
    print(f'ELAPSED TIME = {elapsed_time}')

".\A200795"































