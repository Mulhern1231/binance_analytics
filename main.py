from re import L
import pandas as pd
import os
import numpy
import numpy as np
from scipy.signal import argrelextrema
from operator import itemgetter
from datetime import datetime, timedelta

def extrem(list):
    data = np.array(list)
    idx_minimas = argrelextrema(data, np.less)[0]
    idx_maximas = argrelextrema(data, np.greater)[0]
    idx = np.sort(np.concatenate((idx_minimas, idx_maximas)))
    return data[idx].tolist()


def MaxDrawdown(list):
    xs = np.array(list)
    lp = np.argmax(np.maximum.accumulate(xs) - xs) # end
    pv = np.argmax(xs[:lp]) # start
    return (lp-pv)/pv*100

def summ(list):
    Sum = 0
    for i in list:
        Sum = Sum + i
    return Sum

def delListWord(word ,list, mark=''):
    for i in list:
        word = word.replace(i, mark)
    return word


rez = sorted(os.listdir('StartFile/'))
for item in rez:
    if item[-4:] != '.csv':
        print(f"File {item} does not match")
        continue

    name = delListWord(item, ['TF(', 'Start(','End(','MF(','AMM(','.csv',')', 'D(', 'R(', 'F('])
    name = name.split("_")

    df = pd.read_csv(f"StartFile/{item}")
    df = pd.DataFrame(df)

    GP = 0
    GL = 0

    year = str(0)
    mon = str(0)
    ATM = []
    sum = 1

    NWT1 = 0
    NWTlong = 0
    NWTShort = 0

    NLT1 = 0
    NLTlong = 0
    NLTShort = 0

    time = []
    timeL = []
    timeS = []
    totalFee = []

    AWTDA = []
    AWTBA = []
    AWTDL = []
    AWTBL = []
    AWTDS = []
    AWTBS = []

    ALTDA = []
    ALTBA = []
    ALTDL = []
    ALTBL = []
    ALTDS = []
    ALTBS = []


    RWTA = 0
    RLTA = 0
    RWTS = 0
    RLTS = 0
    RWTL = 0
    RLTL = 0
    MULTI = 0
    for i in range(len(df)):
        if df.loc[i]['type'] == 'multi':
            MULTI += df.loc[i]['pnl']

        if df.loc[i]['pnl'] >= 0:
            GP += df.loc[i]['pnl']
        else:
            GL += df.loc[i]['pnl']
        NT = df.loc[i]['total pnl']
        priceOut = df.loc[i]['price out']
        
        #среднее кол-во сделок в месяц  
        data = df.loc[i]['date enter'].split()[0].split("/")
        if (str(data[2]) != str(year)) or (str(data[1])  != str(mon)):
            ATM.append(sum)
            year = data[2]
            mon = data[1]
            sum = 1
        else:
            sum = sum + 1

        #Number Winning Trades and AWTDA...
        if df.loc[i]['pnl'] >= 0:
            NWT1 += 1
            RWTA += 1
            AWTDA.append(df.loc[i]['pnl/deposit'])
            AWTBA.append(df.loc[i]['pnl/balance'])
            if df.loc[i]['trend (trade type)'] == 'long':
                RWTL += 1
                NWTlong += 1
                AWTDL.append(df.loc[i]['pnl/deposit'])
                AWTBL.append(df.loc[i]['pnl/balance'])
            else:
                RWTS += 1
                NWTShort += 1
                AWTDS.append(df.loc[i]['pnl/deposit'])
                AWTBS.append(df.loc[i]['pnl/balance'])

        #Number Losing Trades
        if df.loc[i]['pnl'] < 0:
            NLT1 += 1
            RLTA += 1
            ALTDA.append(df.loc[i]['pnl/deposit'])
            ALTBA.append(df.loc[i]['pnl/balance'])
            if df.loc[i]['trend (trade type)'] == 'long':
                NLTlong += 1
                RLTL += 1
                ALTDL.append(df.loc[i]['pnl/deposit'])
                ALTBL.append(df.loc[i]['pnl/balance'])
            else:
                NLTShort += 1
                RLTS += 1
                ALTDS.append(df.loc[i]['pnl/deposit'])
                ALTBS.append(df.loc[i]['pnl/balance'])
        
        if df.loc[i]['trend (trade type)'] == 'long':
            d1 = datetime.strptime(df.loc[i]['date enter'].replace(',', '/'), "%m/%d/%Y %H:%M:%S")
            d2 = datetime.strptime(df.loc[i]['date out'].replace(',', '/'), "%m/%d/%Y %H:%M:%S")
            timeL.append(d2 - d1)
        else:
            d1 = datetime.strptime(df.loc[i]['date enter'].replace(',', '/'), "%m/%d/%Y %H:%M:%S")
            d2 = datetime.strptime(df.loc[i]['date out'].replace(',', '/'), "%m/%d/%Y %H:%M:%S")
            timeS.append(d2 - d1)

        totalFee.append(float(df.loc[i]['price enter'])*float(df.loc[i]['volume'])*float(name[17]) + float(df.loc[i]['price out'])*float(df.loc[i]['volume'])*float(name[17]))
        d1 = datetime.strptime(df.loc[i]['date enter'].replace(',', '/'), "%m/%d/%Y %H:%M:%S")
        d2 = datetime.strptime(df.loc[i]['date out'].replace(',', '/'), "%m/%d/%Y %H:%M:%S")
        time.append(d2 - d1) 

    lists = []
    for i in range(len(df)):
        lists.append(float(df.loc[i]['total pnl']))


#ANLTE and MNLTE | AWDD and MWDD
    listExtrem = extrem(lists)
    lens = range(len(listExtrem)-1)
    countMinus = []
    a = listExtrem.pop(0)
    her = []
    dataML = []

    for z in lens:
        b = listExtrem.pop(0)
        for i in lists:
            if i == a:
                a1 = lists.index(i)
            elif i == b:
                b1 = lists.index(i)
        count = 0

        lists2 = []
        for i in range(len(df)):
            lists2.append([df.loc[i]['date out'].split()[0],float(df.loc[i]['total pnl'])])

        for i in lists2[a1:b1+1]:
            if i[1] <= 0:
                count+=1
        countMinus.append(count)

        count2 = 0
        if a < b:
            lowlist = lists2[a1:b1+1]
            date = []
            for i in range(len(lowlist)-1):
                if lowlist[i][0] != lowlist[i+1][0]:
                    date.append(lowlist[i][0])
                    count2 += 1
            dataML.append([date,count2])
            her.append(count2)
        a = b

    ML1 = sorted(dataML, key=itemgetter(1), reverse=True)[0][0][0]+" - "+sorted(dataML, key=itemgetter(1), reverse=True)[1][0][-1]
    ML2 = sorted(dataML, key=itemgetter(1), reverse=True)[1][0][0]+" - "+sorted(dataML, key=itemgetter(1), reverse=True)[1][0][-1]
    ML3 = sorted(dataML, key=itemgetter(1), reverse=True)[2][0][0]+" - "+sorted(dataML, key=itemgetter(1), reverse=True)[2][0][-1]
    ML4 = sorted(dataML, key=itemgetter(1), reverse=True)[3][0][0]+" - "+sorted(dataML, key=itemgetter(1), reverse=True)[3][0][-1]
    ML5 = sorted(dataML, key=itemgetter(1), reverse=True)[4][0][0]+" - "+sorted(dataML, key=itemgetter(1), reverse=True)[4][0][-1] 


    lists = []
    for i in range(len(df)):
        lists.append(float(df.loc[i]['total pnl']))
    a = lists.pop(0)
    perepad = []
    for i in extrem(lists):
        b = [a, lists.pop(0)]
        perepad.append(max(b)-min(b))
        a = lists.pop(0)



    SecondList = {
        "Strategy":  name[0],
        "Coin":      name[1],
        "TF":        name[2],
        "Start":     name[3]+'.'+name[4]+'.'+name[5],
        "End":       name[6]+'.'+name[7]+'.'+name[8],
        "Indicator": name[9][:3],
        "Period":    name[9][3:],
        "MF":        name[10],
        "AMM1":      name[11],
        "AMM2":      name[12],
        "AMM3":      name[13],
        "AMM4":      name[14],
        "Deposit":   name[15],
        "Risk":      name[16],
        "Fee":       name[17],
        "NT":        NT,
        "HOLD":      df.loc[0]['deposit']*((priceOut/df.loc[0]['price out'])-1),
        "MULTI":     MULTI,
        "GP":        GP,
        "GL":        GL,
        "PF":        GP/GL,
        "MD":        MaxDrawdown(extrem(lists)),
        "AD":        numpy.mean(perepad),
        "TT":        len(df),
        "ATM":       numpy.mean(ATM),
        "NWT":       NWT1,
        "NWT_long":  NWTlong,
        "NWT_short": NWTShort,
        "NLT":       NLT1,
        "NLT_long":  NLTlong,
        "NLT_short": NLTShort,
        "ANLTE ":    numpy.mean(countMinus),
        "MNLTE":     max(countMinus),
        "AWDD":      numpy.mean(her),
        "MWDD":      max(her),
        "ML1":       ML1,
        "ML2":       ML2,
        "ML3":       ML3,
        "ML4":       ML4,
        "ML5":       ML5,
        "AWTDA":     numpy.mean(AWTDA),
        "AWTBA":     numpy.mean(AWTBA),
        "AWTDL":     numpy.mean(AWTDL),
        "AWTBL":     numpy.mean(AWTBL),
        "AWTDS":     numpy.mean(AWTDS),
        "AWTBS":     numpy.mean(AWTBS),
        "ALTDA":     numpy.mean(ALTDA),
        "ALTBA":     numpy.mean(ALTBA),
        "ALTDL":     numpy.mean(ALTDL),
        "ALTBL":     numpy.mean(ALTBL),
        "ALTDS":     numpy.mean(ALTDS),
        "ALTBS":     numpy.mean(ALTBS),
        "RWTA | RLTA ": RWTA/RLTA,
        "RWTL | RLTL ": RWTL/RLTL,
        "RWTS | RLTS ": RWTS/RLTS,
        "AHTA":       numpy.mean(time),
        "AHTL":      numpy.mean(timeL),
        "AHTS":      numpy.mean(timeS),
        "FEE":       summ(totalFee),
        
    }

    data = []
    nameData = []
    for i in SecondList:
        nameData.append(i)
        data.append(SecondList[i])

    writer = pd.ExcelWriter(f"ReturnFile/{item.replace('.csv', '')}.xlsx")
    df.to_excel(writer, index=False, sheet_name = "list1")
    pd.DataFrame([data], columns=nameData).to_excel(writer, index=False, sheet_name = "options")
    writer.save() 
    print('DataFrame is written successfully to Excel File.')

