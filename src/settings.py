# -*- coding: UTF-8 -*-
import logging, sys, yaml
from typing import Any

logging.basicConfig(level=logging.INFO, format = "%(asctime)s %(filename)s %(levelname)s:%(message)s")
class Settings:
    def __init__(self) -> None:
        self.__log = logging.getLogger(__name__)
        try:
            with open('conf/config.yml"', 'r') as stream:
                self.__data = yaml.full_load(stream)
        except OSError:
            self.__log.critical('config.yml open failed')
            sys.exit()
        except yaml.YAMLError:
            self.__log.critical('config.yml format error')
            sys.exit()
        except:
            self.__log.critical('config.yml read failed')
            sys.exit()
        if self.__data is None:
            self.__log.critical('config.yml is empty')
            sys.exit()        

    def getConfig(self, key) -> Any | None:
        if key in self.__data:
            return self.__data[key]
        else:
            self.__log.warning('Settings have no key: %s' % key)
            return None 
