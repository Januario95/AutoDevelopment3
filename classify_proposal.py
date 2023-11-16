# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 11:44:53 2022

@author: Januario Cipriano
"""

import os
import logging
import pandas as pd
from enum import Enum
from glob import glob
from datetime import datetime


class Classify(Enum):
    FIRST = 'NWOW'
    SECOND = 'CVU Central'
    


class ClassifyProposal:
    def __init__(self):
        files = glob('*.xlsx')
        self.filename = [file for file in files if file.startswith('Fluxo')][0] # 'Final.xlsx' #  # filename # 'Practice.xlsx'  # 
        self.__df = pd.read_excel(self.filename)
        self.__df.drop_duplicates('Nº', inplace=True)
        
        log_filename = datetime.now().strftime('%d-%b-%Y %H%M%S%z.log')
        logging.basicConfig(filename=f'Logs/Process-Data/Dataframe-{log_filename}',
                            level=logging.WARNING,
                            format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        
    @property
    def dataframe(self):
        # Return the dataframe
        return self.__df

    def update_updated_proposals(self, process_number, collaborator):
        self.__set_index()
        print(f'Setting collaborator\'s name: {collaborator}')
        self.__df.loc[process_number, 'Colaborador'] = collaborator
        self.__df.loc[process_number, 'IsPropostaActualizada'] = False 
        print('Collaborator name set successfully')
        self.__reset_index()
        self.__df.to_excel(os.getcwd() + "/" + self.filename, index=False)

    def get_updated_proposals(self):
        process_numbers = self.__df[
            (self.__df['Estado'] == 'Proposta Atualizada') &
            (self.__df['IsPropostaActualizada'] == True)
        ]
        return process_numbers
    
    def is_updated(self, process_number):
        # Update isUpdated and ModificationEm columns that
        # matches the provided process_number parameter
        # self.__df.set_index('Nº', inplace=True)
        self.__df.loc[process_number, 'IsUpdated'] = True
        self.__df.loc[process_number, 'ModificadoEm'] = datetime.now()
        
    def __reset_index(self):
        # Reset index, as the dataframe is set to have column Nº as 
        # the index for table manupulation purposes
        self.__df.reset_index(inplace=True)

    def __set_index(self):
        self.__df.set_index('Nº', inplace=True)
        
    def save(self, process_number):
        # self.__set_index(self)
        self.is_updated(process_number)
        self.__reset_index()
        # Save the dataframe to local machine as excel file.
        self.__df.to_excel(os.getcwd() + "/" + self.filename, index=False) 
        
    def get_process_numbers(self):
        process_numbers = self.__df[(self.__df['Tipo'].str.contains('Crédito ao Consumo')) & 
                                    (self.__df['IsUpdated'] == False)]['Nº'].tolist()
        return process_numbers
    
    def set_search_results(self, process_number, data):
        logging.warning(f'Searching for PROCESS NUMBER = {process_number}')
        self.__df.set_index('Nº', inplace=True)
        Valor_Requisitado = data.get('Valor_Requisitado')
        Entidade_Patronal = data.get('Entidade-Patronal')
        self.__df.loc[process_number, 'Valor Requisitado'] = Valor_Requisitado
        self.__df.loc[process_number, 'Entidade Patronal'] = Entidade_Patronal
        
        logging.warning(f'Setting Proposal Amount for PROCESS NUMBER = {process_number}')
        self.set_proposal_value(process_number)
        self.set_exceptional_companies(process_number)
        self.save(process_number)
        logging.warning(f'Saving data for PROCESS NUMBER = {process_number}\n')
        
    def set_exceptional_companies(self, process_number):
        if (self.__df.loc[process_number, 'Entidade Patronal'] == 'MLT' or
            self.__df.loc[process_number, 'Entidade Patronal'] == 'CEDSIF'):
            logging.warning(f'Handling exceptional Employer Entity for PROCESS NUMBER = {process_number}')
            self.__df.loc[process_number, 'Area de Verificacao'] = 'CVU Central'

    def set_proposal_value(self, process_number):
        if self.__df.loc[process_number, 'Valor Requisitado'] > 500000:
            self.__df.loc[process_number, 'Area de Verificacao'] = Classify.SECOND.value
        elif self.__df.loc[process_number, 'Valor Requisitado'] == 0:
            pass
        elif self.__df.loc[process_number, 'Valor Requisitado'] <= 500000:
            self.__df.loc[process_number, 'Area de Verificacao'] = Classify.FIRST.value
























