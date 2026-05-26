# -*- coding: UTF-8 -*-
####TODO:
####the Watcher can only run on UNIX-like system
####need to find a cross-platform solution for Windows.
import os, sys, signal, logging

logging.basicConfig(level=logging.INFO, format = "%(asctime)s %(filename)s %(levelname)s:%(message)s")
class Watcher:
    def __init__(self) -> None:
        self.__log = logging.getLogger(__name__)

    def start(self) -> None:
        self.__child = os.fork()
        if self.__child == 0 : return
        else: self.__watch()

    def __watch(self):
        try: os.wait()
        except KeyboardInterrupt:
            self.__log.info("Ctrl-c received! Sending kill to processes.")
            self.__kill()
        sys.exit()

    def __kill(self) -> None:
        try: os.kill(self.__child, signal.SIGKILL)
        except OSError:
            self.__log.error("Kill processes failed!")

