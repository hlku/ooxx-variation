#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
import sys

difficulty = 0

def calculate(tsumeru, limit):
    for i in range(0, 9) : # optimization for only move
        if tsumeru[i] != 0 : continue
        pos = list(tsumeru)
        pos[i] = max(pos) + 1
        if check(pos) : return i # win move!
        pos = list(tsumeru)
        pos[i] = max(pos) + 2
        if check(pos) : return i # be ware!

    solution = set([9])
    value = -100

    for nx in expand(tsumeru) :
        v = findMin(nx, limit, 1, value)
        if value == v :
            solution.add(nx.index(max(nx)))
        elif value < v :
            solution = set([nx.index(max(nx))])
            value = v
    
    print (solution, value) #for debug
    return list(solution)[random.randint(0, len(solution) - 1)]

def findMin(tsumeru, limit, depth, MAX) :
    value = 100
    if check(tsumeru) : return 99 - depth
    elif depth >= limit : return 0
    
    for nx in expand(tsumeru) :
        value = min(value, findMax(nx, limit, depth + 1, value))
        if value < MAX : return value
        
    return value
    
def findMax(tsumeru, limit, depth, MIN) :
    value = -100
    if check(tsumeru) : return -99 + depth
    elif depth >= limit : return 0
    
    for nx in expand(tsumeru) :
        value = max(value, findMin(nx, limit, depth + 1, value))
        if value > MIN : return value
        
    return value

def expand(pos) :
    def rotate(t) :
        return [t[6], t[3], t[0], t[7], t[4], t[1], t[8], t[5], t[2]]
    def mirror(t) :
        return [t[2], t[1], t[0], t[5], t[4], t[3], t[8], t[7], t[6]]
    biggest = max(pos)
    ret = []
    for i in range(0, 9) :
        if pos[i] == 0 :
            tmp = list(pos)
            tmp[i] = biggest + 1
            fresh(tmp)
            if tmp.count(0) > 3 :
                if rotate(tmp) in ret or \
                   rotate(rotate(tmp)) in ret or \
                   rotate(rotate(rotate(tmp))) in ret or \
                   mirror(tmp) in ret or \
                   mirror(rotate(tmp)) in ret or \
                   mirror(rotate(rotate(tmp))) in ret or \
                   mirror(rotate(rotate(rotate(tmp)))) in ret : pass
                else : ret.append(tmp)
            else : ret.append(tmp)
    return ret

def fresh(board) :
    if max(board) == 8 and board.count(2) == 0 : pass
    elif board.count(0) < 3 or (max(board) == 7 and board.count(2) == 0):
        tmp = list()
        for i in board:
            if i == 0 : tmp.append(99)
            else : tmp.append(i)
        board[tmp.index(min(tmp))] = 0

def check(board) :
    k = lambda a, b, c : True if \
        (board[a] % 2 == board[b] % 2 == board[c] % 2) and \
        board[a] != 0 and board[b] != 0 and board[c] != 0 \
        else False
    if k(0, 1, 2) or k(3, 4, 5) or k(6, 7, 8) or k(0, 3, 6) or \
       k(1, 4, 7) or k(2, 5, 8) or k(0, 4, 8) or k(2, 4, 6) : return True
    return False

def play(board, step, add = 1) :
    board[step] = max(board) + add
    fresh(board)
    
def display(board) :
    global difficulty
    q = list()
    for i in board :
        if i == 0 : q.append('  ')
        else :
            if difficulty < 3 :
                k = '%2d' % tuple([i])
                if i % 2 == 1: k2 = '\033[1;32m' + k + '\033[0m'
                else : k2 = '\033[1;36m' + k + '\033[0m'
                q.append(k2)
            elif difficulty < 5 : q.append('%2d' % tuple([i]))
            else :
                if i % 2 == 1 : q.append('Ｏ')
                else : q.append('Ｘ')
                
    if max(board) != 0 :
        q[board.index(max(board))] = \
            '\033[41m' + q[board.index(max(board))] + '\033[0m'
    p = '''\
+--+--+--+
|%s|%s|%s|
+--+--+--+
|%s|%s|%s|
+--+--+--+
|%s|%s|%s|
+--+--+--+
'''
    print '\n' + p % tuple(q), 

def main():
    global difficulty
    while True:
        print "choose computer's level"
        print '\t3~4 play with 1 color, 5~6 play without numbers'
        print '\tlevel 0, computer thinks 3 steps'
        print '\twith each higher level, computer thinks more 2 steps'
        difficulty = int(raw_input('level : '))
        if difficulty < 0 or difficulty > 6 :
            print 'error input!'
            continue
        else :
            hard = 3 + difficulty * 2
            break
        
    while True:
        print '\nchoose a mode'
        print '\t-2 : computer start with 2 steps'
        print '\t-1 : computer go first'
        print '\t 0 : random'
        print '\t 1 : you go first'
        print '\t 2 : you start with 2 steps'
        mode = int(raw_input('mode : '))
        if mode < -2 or mode > 2 :
            print 'error input!'
            continue
        else : break
    
    board = [0] * 9
    if mode == -2 :
        play(board, calculate(board, hard))
        play(board, calculate(board, hard), 2)
    elif mode == -1 :
        play(board, calculate(board, hard))
    elif mode == 0 and random.randint(0, 1) == 0:
        play(board, calculate(board, hard))
        
    while True:
        display(board)
        if check(board) :
            print 'computer win!'
            break
        elif max(board) >= 50 :
            print 'tie!'
            break
        step = int(raw_input('input the position (1-9): ')) - 1
        if step < 0 or step > 8 or board[step] != 0 :
            print "illegal!!"
            continue
        if mode == 2 and max(board) == 1:
            play(board, step, 2)
        else :
            play(board, step)
        if mode == 2 and max(board) == 1:
            continue
        display(board)
        if check(board) :
            print 'you win!'
            break
        play(board, calculate(board, hard))

if __name__ == '__main__':
    main()
