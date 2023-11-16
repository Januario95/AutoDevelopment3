import os
import json
import numpy as np
import pandas as pd
from glob import glob
from enum import Enum
from datetime import datetime


class NodeStructure:
    COUNT = 0
    def __init__(self, timer, nProcesso, tipoConta, nome, Segmento,
                 estado, branch, user, R, CreationDate, ModificadoEm,
                 ValorRequisitado, Colaborador2, EntidadePatronal, IsUpdated,
                 IsPropostaActualizada):
        self.timer = timer
        self.nProcesso = nProcesso
        self.tipoConta = tipoConta
        self.nome = nome
        self.Segmento = Segmento
        self.estado = estado
        self.branch = branch
        self.user = user
        self.R = R
        self.CreationDate = CreationDate
        self.ModificadoEm = ModificadoEm
        self.ValorRequisitado = ValorRequisitado
        self.Colaborador2 = Colaborador2
        self.EntidadePatronal = EntidadePatronal
        self.IsUpdated = IsUpdated
        self.IsPropostaActualizada = IsPropostaActualizada
        NodeStructure.COUNT += 1
        
    def __str__(self):
        return f'Node-{self.COUNT}'
        
    @property
    def values(self):
        return {
            'sla': self.timer,
            'process_number': self.nProcesso,
            'type': self.tipoConta, 
            'name': self.nome,
            'segment': self.Segmento,
            'state': self.estado,
            'branch': self.branch,
            'user': self.user,
            'R': self.R,
            'creation_date': self.CreationDate, 
            'Modificado-Em': self.ModificadoEm,
            'ValorRequisitado': self.ValorRequisitado,
            'Colaborador2': self.Colaborador2,
            'EntidadePatronal':  self.EntidadePatronal,
            'IsUpdated': self.IsUpdated,
            'IsPropostaActualizada': self.IsPropostaActualizada
        }
        

class ADT:
    def __init__(self, nodes=[]):
        self.__data = []
        self.PAGE_COUNT = 0
        self.IS_PROPOSTA_ATUALIZADA = False
        for node in nodes:
            self.__raise_on_error(node)
            self.__data.append(node)
            
    def __str__(self):
        return f'<ADT ({len(self.__data)} Nodes)>'
    
    def __len__(self):
        return len(self.__data)
        
    def push(self, nodes):
        if isinstance(nodes, list):
            for node in nodes:
                self.__raise_on_error(node)
                self.__data.append(node)
        else:
            self.__raise_on_error(nodes)
            self.__data.append(nodes)
            
    def __raise_on_error(self, node):
        if not isinstance(node, NodeStructure):
            raise TypeError('Node must be an instance of NodeStructure')
        
    @property
    def data(self):
        return [node.values for node in self.__data]

    





    



















