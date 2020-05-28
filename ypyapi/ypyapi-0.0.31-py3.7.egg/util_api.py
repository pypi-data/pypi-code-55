#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/5/25 17:05
# @Author : yangpingyan@gmail.com
import sqlalchemy

import numpy as np
import matplotlib.pyplot as plt

def kelly_formula_stock():
    probability_win = 0.7
    probability_loss = 1 - probability_win
    ratio_win = 1.5
    ratio_loss = 0.8
    kelly = probability_win/ratio_loss - probability_loss/ratio_win



    print("Kelly is", kelly)
    players = 100
    times = 50
    winners = 0
    balance = 0.0
    for j in range(players):
        m = np.zeros(times)
        m[0] = 100.0
        for i in range(1, times):
            if np.random.randint(2):
                m[i] = m[i - 1] * ratio_win * kelly + m[i - 1] * (1 - kelly)
            else:
                m[i] = m[i - 1] * ratio_loss * kelly + m[i - 1] * (1 - kelly)

        if m[-1] > m[0]:
            winners += 1
        if m[-1] > balance:
            balance = m[-1]
        plt.semilogy(m)

    print('The number of winners is', winners)
    print(balance)
    plt.xlabel('Times')
    plt.ylabel('Balance')
    plt.show()

    return kelly


if __name__ == '__main__':
    print("Mission start!")
    kelly_formula_stock()
    print("Mission complete!")
