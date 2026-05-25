#!/usr/bin/python
# -*- coding: UTF-8 -*-

import src.ooxx, src.watcher

if __name__ == '__main__':
    watcher = src.watcher.Watcher()
    watcher.start()

    ooxx = src.ooxx.OOXX()
    while True: #forever playing until Ctrl+c
        ooxx.start()
   