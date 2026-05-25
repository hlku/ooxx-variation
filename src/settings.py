# -*- coding: UTF-8 -*-
import logging, sys, yaml
from typing import Any

logging.basicConfig(level=logging.INFO, format = "%(asctime)s %(filename)s %(levelname)s:%(message)s")
class Settings:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        try:
            with open('conf/config.yml"', 'r') as stream:
                self.data = yaml.full_load(stream)
        except OSError:
            self.log.critical('config.yml open failed')
            sys.exit()
        except yaml.YAMLError:
            self.log.critical('config.yml format error')
            sys.exit()
        except:
            self.log.critical('config.yml read failed')
            sys.exit()
        if self.data is None:
            self.log.critical('config.yml is empty')
            sys.exit()
            
        if self.getConfig('debug'):
            self.log.setLevel(logging.DEBUG)
            self.log.debug('Debug mode is on')            

    def getConfig(self, key) -> Any | None:
        if key in self.data:
            return self.data[key]
        else:
            self.log.warning('Settings have no key: %s' % key)
            return None 
