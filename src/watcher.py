# -*- coding: UTF-8 -*-
import logging, multiprocessing, time, sys, os, signal

logging.basicConfig(level=logging.INFO, format = "%(asctime)s %(filename)s %(levelname)s:%(message)s")
class Watcher:
    def __init__(self) -> None:
        """init with a logger"""
        self.__log = logging.getLogger(__name__)

    def start(self) -> None:
        """start a multiprocess watcher,
           child process catches keyboard interrupt and kills all processes
           parent do nothing, just return to __main___ to do game"""
        #fork is only available on Unix. using spawn can run on both Unix and Windows
        multiprocessing.set_start_method('spawn')

        #new process, child do watching, parent go game
        child = multiprocessing.Process(target = self.watch, name = "Watcher", daemon = True)
        child.start()
        #parent process will reach here and return to __main__ to do game

    def watch(self): #can't write as __watch, because multiprocessing class can't see it
        """child process do watching, if receive keyboard interrupt, kill all processes"""
        try:
            while True: time.sleep(1) #do nothing, just wait for keyboard interrupt
        except KeyboardInterrupt:
            self.__log.info("Ctrl-c received! Sending kill to parent process.")
            self.__kill()
        except Exception as e:
            self.__log.warning("Unexpected error: %s", e)

    def __kill(self) -> None:
        """force kill all processes"""
        try:
            parent = multiprocessing.parent_process() #get parent process
            self.__log.debug("Parent process: %s", str(parent.pid))
            os.kill(parent.pid, signal.SIGTERM) #ask parent process normally terminate
            if parent.is_alive() and hasattr(signal, 'SIGKILL'): #only UNIX has SIGKILL
                os.kill(parent.pid, signal.SIGKILL) #can't normally terminate, force kill
        except Exception as e:
            self.__log.error("Kill parent process failed: %s", e)
        finally:
            sys.exit(0) #after killing parent process, suiciding
