'''
Created on 12/04/2013

@author: Manuel Delgado
'''

class Amulet:
    '''
    classdocs
    '''
    _healer = None


    def __init__(self, healer):
        '''
        Constructor
        '''
        self._healer = healer
    
    def is_checksum_file(self, filename):
        raise NotImplementedError
        
    def check_with(self, filepath):
        raise NotImplementedError
     
