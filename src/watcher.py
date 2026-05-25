# -*- coding: UTF-8 -*-
import os, sys, signal, logging

logging.basicConfig(level=logging.DEBUG, format = "%(asctime)s %(filename)s %(levelname)s:%(message)s")
class Watcher:
    def __init__(self) -> None:        
        self.log = logging.getLogger(__name__)
        self.child = os.fork()
        if self.child == 0 : return
        else: self.watch()

    def watch(self):
        try: os.wait()
        except KeyboardInterrupt:
            self.log.info("Ctrl-c received! Sending kill to threads.")
            self.kill()
        sys.exit()

    def kill(self) -> None:
        try: os.kill(self.child, signal.SIGKILL)
        except OSError: pass

