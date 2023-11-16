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
from selenium.webdriver.support import expected_conditions as EC

from instantiate_driver import initiate_driver
from data_structure import ADT, NodeStructure

# URL = 'http://10.245.87.77/itcore.sites/ITCore.Ui.Web/ITCore.aspx'

# BOOK = "https://www.scribd.com/book/163559831/Fortune-Favors-the-Bold-What-We-Must-Do-to-Build-a-New-and-Lasting-Global-Prosperity"

# driver = initiate_driver()

# driver.get(URL)

# WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "MainIframe")))
# driver.switch_to.frame(driver.find_element(By.ID, "MainIframe"))

# dept_processes = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_fwcInit_BtnDepartmentWorklist"]')
# dept_processes.click()
# time.sleep(10)

# print('Starting...')

adt = ADT()


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

def refresh_page():
    print('REFRESHING PAGE....')
    time.sleep(2)
    driver.refresh()
    time.sleep(7)
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "MainIframe")))
    driver.switch_to.frame(driver.find_element(By.ID, "MainIframe"))


def refresh_page2():
    print('REFRESHING PAGE....')
    time.sleep(2)
    driver.refresh()
    time.sleep(7)
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "MainIframe")))
    driver.switch_to.frame(driver.find_element(By.ID, "MainIframe"))

    dept_processes = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_fwcInit_BtnDepartmentWorklist"]')
    dept_processes.click()
    time.sleep(10)


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

    print(f"ESTADO = {row_data['estado']}")
    if row_data['estado'] == 'Proposta Atualizada':
         row_data['IsPropostaActualizada'] = True

    adt.IS_PROPOSTA_ATUALIZADA = False
    node = NodeStructure(**row_data)
    print(node.values['state'])

    print(node.values)
    print('\n')
    adt.push(node)


".\A200795"


def fetch_table():
    logging.warning(f'Fetching page {adt.PAGE_COUNT}')
    adt.PAGE_COUNT += 1
    for path_id in range(0, 15):
        try:
            start = datetime.now().strftime('%d-%b-%Y %H:%M:%S')
            get_row(path_id)
            end = datetime.now().strftime('%d-%b-%Y %H:%M:%S')
            logging.warning(f'Fetching row {path_id+1}. \tStarted at {start}. \tEnded at: {end}')
            # time.sleep(0.3)
            driver.save_screenshot('Page1.png')
        except Exception as exc:
            print(exc)
            logging.warning(exc)
    logging.warning('\n')
    time.sleep(3)
    print('\n')
    
        
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
        except Exception as exc:
            print(exc)
            logging.warning(exc)
    

def save_to_excel():
    df = pd.DataFrame(adt.data)
    df.columns = 'SLA, Nº, Tipo, Nome, Segmento, Estado, Balcão de Criação, Colaborador, R, Dt. Criação, DownloadedAt, Valor Requisitado, Area de Verificacao, Entidade Patronal, IsUpdated, IsPropostaActualizada'.split(', ')
    now = datetime.now()
    now = now.strftime('%d-%b-%Y %H%M%S')
    filename = f'Processos-{now}.xlsx'

    df.drop_duplicates('Nº', inplace=True)
    
    process_numbers = df['Nº'].to_list()
    df.set_index('Nº', inplace=True)
    
    for process_number in process_numbers:        
        if df.loc[process_number, 'Segmento'] == 'Staff':
            df.loc[process_number, 'Nome'] = ''
            
    df.reset_index(inplace=True)
    df.to_excel(filename, index=False)
    time.sleep(2)


def move_older_files():
    files = glob('Logs/Fetch-Data/*.log')
    if len(files) > 0:
        path = Path(files[0])
        if path.exists():
            filename = path.name
            shutil.move(files[0], f'Logs/Fetch-Data/Old-Logs/{filename}')


def main():
    move_older_files()

    filename = datetime.now().strftime('%d-%b-%Y %H%M%S%z.log')
    logging.basicConfig(filename=f'Logs/Fetch-Data/{filename}',
                        level=logging.WARNING,
                        format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')

    logging.warning('Started to fetch data.')
    fetch_table()
    
    fetch_remaining_pages()
    
    save_to_excel()
    
    # driver.close()
    time.sleep(2)


def fetch_table_page(page_id):
    for td_id in range(0, 15):
        try:
            # driver = start_driver()
            link = driver.find_element(By.XPATH, f'//*[@id="ContentPlaceHolder1_flwForm_fwcInit_grvPager_repPager_pb1_{page_id}"]')
            print(f'LINK ID: {link.text}')
            link.click()
            time.sleep(7)

            get_row(td_id)
            if adt.IS_PROPOSTA_ATUALIZADA:
                print('\nIS_PROPOSTA_ATUALIZADA\n')
                time.sleep(35)
            else:
                print('\nNOT IS_PROPOSTA_ATUALIZADA\n')
                time.sleep(3)
        except Exception as e:
            pass


def run_all():
    # '//*[@id="ContentPlaceHolder1_flwForm_fwcInit_grvPager_repPager_pb1_0"]' 
    for i in range(6):
        t = threading.Thread(target=fetch_table_page, args =[i])
        t.start()


".\A200795"

if __name__=='__main__':
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


".\A200795"































