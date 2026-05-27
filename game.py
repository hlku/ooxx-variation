#!/usr/bin/python
# -*- coding: UTF-8 -*-

import src.ooxx, src.watcher

if __name__ == '__main__':
    watcher = src.watcher.Watcher() #a watcher to catch keyboard interrupt
    watcher.start()

    ooxx = src.ooxx.OOXX()
    while ooxx.start(): pass #keep playing until player says no or watcher kills the process
