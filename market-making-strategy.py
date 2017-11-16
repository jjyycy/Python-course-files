from qpython import qconnection
import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

def qSym(sym):
    return "`" + sym
  
def tsfmt(x):
    if x >= 0:
        return '0D%02d:00:00'%(x)
    else:
        return '-0D%02d:00:00'%(-x)

class MarketMakingStrategy(object):
    def __init__(self, db, d, sym, tL=-7, tR=16, maxPos=100, nmax = 0):
        self.db = db
        self.d = d
        self.sym = sym
        self.tL = tL
        self.tR = tR
        self.maxPos  = maxPos
        self.nmax    = nmax
        
    def queryData(self):
        query = "select from tqmergeT[" + self.d.strftime("%Y.%m.%d") + ";" + qSym(self.sym) +";" + tsfmt(self.tL) + ';' + tsfmt(self.tR) + "] where (differ bid)|(differ ask)"
        print(query)
        self.marketData  = self.db(query)
        query = 'select minpxincr, dispfactor, notional from instinfo where inst =sym2inst[' + qSym(self.sym) +']'
        print(query)
        contractSpec = self.db(query)
        self.pTick = contractSpec.minpxincr[0]
        self.dispfactor = contractSpec.dispfactor[0]
        self.notional = contractSpec.notional[0]
        self.x = 0
        self.P = 0
        self.M = 0.5 * (self.marketData.bid[0] + self.marketData.ask[0])
        self.bPrice = np.nan
        self.aPrice = np.nan
        self.bSize = np.nan
        self.aSize = np.nan
        self.tradeTime     = [min(self.marketData.t)]
        self.curPos     = [self.x]
        self.curCashFlow   = [self.P]
        self.curMidPrice   = [self.M]
    
    def trade(self, tseq, tTime, ssiz, mid, prc):
        if pd.isnull(prc): # quote
            if ssiz > 0:
                prc = self.bPrice
                self.bPrice = np.nan
            else:
                prc = self.aPrice
                self.aPrice = np.nan
            self.x += ssiz
            self.P -= ssiz * prc
            self.tradeTime.append(tTime)
            self.curPos.append(self.x)
            self.curCashFlow.append(self.P)
            self.curMidPrice.append(mid)
            
    def runStrategy(self):
        bPrev, bsPrev, aPrev, asPrev = np.nan, np.nan, np.nan, np.nan
        for curdata in self.marketData.itertuples():
            if pd.isnull(curdata.prc):
                pmid = 0.5 * (curdata.bid + curdata.ask)
                
                if not pd.isnull(self.bPrice):
                    if curdata.bid < self.bPrice:
                        self.trade(curdata.seq, curdata.t, +1, pmid, np.nan)
                    elif curdata.bid > self.bPrice:
                        self.bPrice = np.nan
                        
                if not pd.isnull(self.aPrice):
                    if curdata.ask > self.aPrice:
                        self.trade(curdata.seq, curdata.t, -1, pmid, np.nan)
                    elif curdata.ask < self.aPrice:
                        self.aPrice = np.nan
                    bPrev, bsPrev, aPrev, asPrev = curdata.bid, curdata.bsiz, curdata.ask,curdata.asiz
        
            else:
                pmid = 0.5 * (bPrev + aPrev)
                
                if not pd.isnull(self.bPrice):
                    if curdata.prc < self.bPrice:
                        self.trade(curdata.seq, curdata.t, +1, pmid, np.nan)
                    elif curdata.prc  == self.bPrice:
                        self.bSize = self.bSize - curdata.siz
                    if self.bSize < 0:
                        self.trade(curdata.seq, curdata.t, +1, pmid, np.nan)
                        
                if not pd.isnull(self.aPrice):
                    if curdata.prc > self.aPrice:
                        self.trade(curdata.seq, curdata.t, -1, pmid, np.nan)
                    elif curdata.prc  == self.aPrice:
                        self.aSize = self.aSize - curdata.siz
                    if self.aSize < 0:
                        self.trade(curdata.seq, curdata.t, -1, pmid, np.nan)
                    
            if pd.isnull(self.bPrice) and self.x < self.maxPos:
                self.bPrice, self.bSize = bPrev, bsPrev
                
            if pd.isnull(self.aPrice) and self.x > - self.maxPos:
                self.aPrice, self.aSize = aPrev, asPrev
                
            self.trade(max(self.marketData.seq), max(self.marketData.t), -self.x,bPrev if self.x > 0 else aPrev, 0.5 * (bPrev + aPrev))
            self.res = pd.DataFrame({'tradeTime': self.tradeTime, 'position': self.curPos, 'cashFlow': self.curCashFlow, 'midPrice': self.curMidPrice})
            self.res['PnL'] = self.res.cashFlow + self.res.position * self.res.midPrice
    
    def plot(self):
        plt.figure(figsize = (8,6))
        plt.subplot(311)
        plt.plot(self.res.tradeTime, self.res.midPrice, linewidth=.5, color='b')
        plt.ylabel('Mid Price')
        plt.title('{} on {}, maxpos {}, notional {:.0f}'.format(self.sym, self.d,self.maxPos, self.notional))
        plt.subplot(312)
        plt.plot(self.res.tradeTime, self.res.position, linewidth=.5, color='r')
        plt.plot(self.res.tradeTime, np.zeros(self.res.tradeTime.shape), linewidth =.5, color='k')
        plt.ylabel('Position')
        plt.subplot(313)
        plt.plot(self.res.tradeTime, self.res.PnL, linewidth=.5, color='g')
        plt.plot(self.res.tradeTime, np.zeros(self.res.tradeTime.shape), linewidth =.5, color='k')
        plt.ylabel('Mark-to-market P&L')
        plt.savefig('MMResult.png')
        plt.show()
        
def main():
    curDT = datetime.datetime.now()
    db_IR = qconnection.QConnection(host='kx', port=6000, pandas = True)
  
    # initialize connection
    db_IR.open()
    d = datetime.date(2017, 8, 23) 
    sym = 'ZNU7'
    tL =6
    tR = 16
    maxPos = 100 
    nmax =0
    mms = MarketMakingStrategy(db_IR, d, sym, tL, tR, maxPos, nmax)
    mms.queryData()
    mms.runStrategy()
    mms.plot()
    print(datetime.datetime.now() - curDT)
    
if __name__ == '__main__':
    main()
