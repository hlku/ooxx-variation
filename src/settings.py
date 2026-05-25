# -*- coding: UTF-8 -*-
import logging, sys, yaml
from typing import Any

logging.basicConfig(level=logging.INFO, format = "%(asctime)s %(filename)s %(levelname)s:%(message)s")
class Settings:
    """Class to handle the settings of the game."""
    def __init__(self) -> None:
        """Initialize the settings by reading the config.yml file."""
        self.__log = logging.getLogger(__name__)
        try:
            with open('conf/config.yml"', 'r') as stream:
                self.__data = yaml.full_load(stream)
            self.check()
        except OSError:
            self.__log.error('config.yml open failed')
            self.setDefault()
        except yaml.YAMLError:
            self.__log.error('config.yml format error')
            self.setDefault()
        except:
            self.__log.error('config.yml read failed')
            self.setDefault()
    
    def setDefault(self) -> None:
        """If the yaml file read fails, set default values."""
        self.__data = {
            'engine': 'AlphaBeta',
            'level': {'mc': 5000, 'ab': 4},
            'display': 0,
            'debug': False
        }

    def check(self):
        """Check the settings for validity.
        If any setting is invalid, log an error, and use default value."""

        if self.__data is None: 
            self.__log.error('config.yml is empty')
            self.setDefault()
            return

        engine = self.getConfig('engine')
        match engine:
            case 'mc': self.__data['engine'] = 'MonteCarlo'
            case 'ab': self.__data['engine'] = 'AlphaBeta'
            case 'MonteCarlo' | 'AlphaBeta' : pass
            case _:
                self.__log.error('Unknown engine: %s' % engine)
                self.__data['engine'] = 'AlphaBeta' #default to AlphaBeta

        level = self.getConfig('level') 
        if level is None or not isinstance(level, dict):
            self.__log.error('Level value is not set or invalid')
            self.__data['level'] = {'mc': 5000, 'ab': 4} #default level
        else:
            if level['mc'] is None or not isinstance(level['mc'], int) or level['mc'] <= 0:
                self.__log.error('MonteCarlo level is invalid')
                self.__data['level']['mc'] = 5000 #default MonteCarlo level
            if level['ab'] is None or not isinstance(level['ab'], int) or level['ab'] < 0:
                self.__log.error('AlphaBeta level is invalid')
                self.__data['level']['ab'] = 4 #default AlphaBeta level
        
        display = self.getConfig('display')
        if display is None or not isinstance(display, int):
            self.__log.error('Display value is invalid')
            self.__data['display'] = 0 #default display mode
        elif display < 0 or display > 2:
            self.__log.error('Display value should be 0, 1, or 2')
            self.__data['display'] = 0 #default display mode
        
        debug = self.getConfig('debug')
        if debug is None or not isinstance(debug, bool):
            self.__log.error('Debug value is invalid')
            self.__data['debug'] = False #default no debugging

    def getConfig(self, key:str) -> Any | None:
        """Get the value of a setting by key."""
        if key in self.__data:
            return self.__data[key]
        else:
            self.__log.warning('Settings have no key: %s' % key)
            return None 
