from math import *

class EuropeanCallOption:
    class _Price:
        stockPrice = 0.0
        optionPrice = 0.0
        def __init__(self):
            self.stockPrice = 0.0
            self.optionPrice = 0.0
        def __str__(self):
            return str((self.stockPrice, self.optionPrice))
    def __init__(self, S0, K, r, sigma, T):
        self._S0 = S0
        self._K = K
        self._r = r
        self._sigma = sigma
        self._T = T
    def __str__(self):
        return ('EuropeanCallOption(' + str(self._S0) + ','
                + str(self._K) + ',' + str(self._r) + ','
                + str(self._sigma) + ',' + str(self._T) + ')')
    def binomialPrice(self, numIntervals):
        deltaT = self._T / numIntervals
        u = exp(self._sigma * sqrt(deltaT))
        d = 1 / u
        a = exp(self._r * deltaT)
        p = (a - d) / (u - d)
        q = 1 - p
        # fill tree with all 0.0s
        self._binomialTree = []
        for i in range(numIntervals + 1):
            level_vec = []
            for j in range(i + 1):
                level_vec.append(self._Price())
            self._binomialTree.append(level_vec)
        if numIntervals < 10:
            print('\nAfter filled in with all 0.0:')
            self.binomialTreePretty()
        # fill tree with stock prices
        for i in range(numIntervals + 1):
            for j in range(i + 1):
                self._binomialTree[i][j].stockPrice = (
                        self._S0 * u ** j * d ** (i-j))
        if numIntervals < 10:
            print('\nAfter filled in with stock prices:')
            self.binomialTreePretty()
        # fill in terminal node option prices
        for j in range(numIntervals + 1):
            self._binomialTree[numIntervals][j].optionPrice = (
                max(self._binomialTree[numIntervals][j].stockPrice - self._K,
                            0.0))
        if numIntervals < 10:
            print('\nAfter filled in with terminal option values:')
            self.binomialTreePretty()
        # work backwards, filling optionPrices in the rest of the tree
        for i in range(numIntervals - 1, -1, -1):
            for j in range(i + 1):
                self._binomialTree[i][j].optionPrice = (
                    exp(-self._r * deltaT)
                    * (p * self._binomialTree[i+1][j+1].optionPrice
                       + q * self._binomialTree[i+1][j].optionPrice))
        if numIntervals < 10:
            print('\nAfter filled in with all option values:')
            self.binomialTreePretty()
        return self._binomialTree[0][0].optionPrice
    def binomialTreePretty(self):
        nlevels = len(self._binomialTree)
        if nlevels < 10:
            print('\nBinomialTree with', nlevels - 1, 'time steps:')
            for row in range(nlevels):
                print('\nStock:  ', end='')
                ncols = len(self._binomialTree[row])
                for col in range(ncols):
                    print('{:8.4f}'.format(self._binomialTree[row][col].stockPrice), end='')
                print('')
                print('Option: ', end='')
                for col in range(ncols):
                    print('{:8.4f}'.format(self._binomialTree[row][col].optionPrice), end='')
                print('')
            print('')

ec = EuropeanCallOption(50.0, 50.0, 0.1, 0.4, 0.4167)

for steps in [5,10,20,50,100,200,500,1000]:
    print('Call price, with', steps, 'intervals:', round(ec.binomialPrice(steps), 4))

    
