'''
Created on 18/04/2013

@author: manuel
'''

import ConfigParser

config = ConfigParser.RawConfigParser()
config.add_section('log')
config.set('log', 'level', 'debug')
config.set('log', 'file', 'healer.log')
config.add_section('repo')
config.set('repo', 'path', './TEST/')
config.set('repo', 'amulet', 'debian')
config.set('repo', 'mirror', 'http://archive.ubuntu.com/ubuntu/')
with open('ubuntu.cfg', 'wb') as configfile:
    config.write(configfile)
