'''
Created on 10/04/2013

@author: Manuel Delgado

RepoHealer is a Python script to repair Software repository packages using checksum files.
It uses plugins called Amulets to check a given repository and repair the packages with bad checksums
Based on MD5 repo-check script first developed by Luis Zarate in 2011

TODO:
    Create more Amulets
    Check if class inherites from Amulet
'''
import inspect, logging, os
from ConfigParser import ConfigParser

class RepoHealer:
    '''
    classdocs
    '''
    LOG_LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}
    
    _amulet = None
    _logger = None
    _repobase = ""
    _mirror = ""

    def __init__(self, reponame = None):
        '''
        Constructor
        '''
        if reponame is not None:
            self.load_config(reponame)   
        else:
            logging.basicConfig(level=self.LOG_LEVELS.get('debug', logging.NOTSET))
            self._logger = logging.getLogger("HealerLogger.NoRepo")
            logging.error("No repo name set, use set_config or define a repo")       

    @property
    def repobase(self):
        '''Get the base path for the repo'''
        return self._repobase

    @property
    def mirror(self):
        '''Get the url for the mirror'''
        return self._mirror
    
    @property
    def logging(self):
        return self._logger
    
    def set_config(self, repopath, repotype, mirror):
        '''
        Set config parameters
        '''
        self._repobase = repopath
        self._mirror = mirror
        
        module = __import__("amulets."+repotype, fromlist=[repotype.capitalize()])
        amuletClass = getattr(module, repotype.capitalize())
        if inspect.isclass(amuletClass):
            #TODO Check if inherites from Amulet
            logging.info("Using " + repotype + " Amulet")
            self._amulet = amuletClass(self)
        else:
            logging.error("Not a valid Amulet: " + repotype)
        
    
    def load_config(self, reponame):
        '''
        Load Config from file
        '''
        configpath = os.path.join('./config/', reponame + '.cfg')
        if os.path.exists(configpath):
            config = ConfigParser()
            config.read(configpath)
            loglevel = config.get('log', 'level')
            logfile = config.get('log', 'file')
            repopath = config.get('repo', 'path')
            repotype = config.get('repo', 'amulet')
            mirror = config.get('repo', 'mirror')
            logging.basicConfig(filename=logfile,level=self.LOG_LEVELS.get(loglevel, logging.NOTSET))
            self._logger = logging.getLogger("HealerLogger."+reponame)
            self.set_config(repopath, repotype, mirror)
        else:
            logging.basicConfig(level=self.LOG_LEVELS.get('debug', logging.NOTSET))
            self._logger = logging.getLogger("HealerLogger.NoRepo")
            logging.critical("No config file for the repo")
    
    def _recursive_search(self, path):
        dirlist = os.listdir(path)
        for innerpack in dirlist:
            nextPath = os.path.join(path, innerpack)
            if self._amulet.is_checksum_file(innerpack):
                logging.info("Searching in: " + nextPath)
                self._amulet.check_with(nextPath)
            else:
                # Prevent /ubuntu/ubuntu/...
                if innerpack != os.path.basename(path) and os.path.isdir(nextPath):
                    self._recursive_search(nextPath)
                    
    def start (self):
        if self._amulet is not None:
            logging.info("Starting process...")
            self._recursive_search(self._repobase)
            logging.info("Finish healing")
        else:
            logging.critical("No Healer!")

def main ():
    repohealer = RepoHealer("ubuntu")
    repohealer.start()
    
main()
