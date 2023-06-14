import csv
import datetime
import calendar

symbol = ["AORD", "BVSP", "FCHI", "FTSE", "GDAXI", "GSPTSE", "HSI", "KS11", "N225", "NSEI", "SPX", "SSEC", "SSMI"]
month = [0, 31, 28,31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def csv2json(filename):
    with open("./data/"+filename, mode='r', encoding='utf-8-sig') as f:
        table = csv.DictReader(f)
        data = []
        for line in table:
            if line == None:
                break
            line = dict(line)
            day = line['date'].split(' ')[0]
            data.append({'date': day, 'rv5': line['rv5']})
    # print(data)
    return data
    
    
def json2csv(data, filename):
    with open("./result/"+filename+"_result.csv", mode='w', encoding='utf-8', newline='') as f:
        headers = ["date", "Symbol", "rv5", "begin|end"]
        writer = csv.DictWriter(f, fieldnames=headers)
        for line in data:
            writer.writerow(line)
            
if __name__ == '__main__':
    startDay = datetime.datetime.strptime("2011-03-11", "%Y-%m-%d")
    endDay = datetime.datetime.strptime("2022-11-28", "%Y-%m-%d")
    # print(startDay+datetime.timedelta(days=31))
    # print(startDay+datetime.timedelta(days=7))
    
    for sym in symbol:
        filename = sym + ".csv"
        data = csv2json(filename)
        result = []
        i = 0
        tagDay = startDay
        print(sym)
        while tagDay < endDay:
            # print(tagDay, i)
            row = {'date': str(tagDay).split(' ')[0], 'Symbol': sym, 'rv5': 0, 'begin|end':""}
            sumRV5 = 0
            validDay = 0 
            while i < len(data):
                canDay = datetime.datetime.strptime(data[i]['date'], "%Y-%m-%d")
                if canDay == tagDay:
                    mon = int(str(tagDay).split('-')[1])
                    adds = month[mon]
                    if mon==2:
                        year = int(str(tagDay).split('-')[0])
                        if year==2012 or year==2016 or year==2020:
                            adds += 1
                    for j in range(i, i+31):
                        if j >= len(data):
                            break
                        day = datetime.datetime.strptime(data[j]['date'], "%Y-%m-%d")
                        if (day-tagDay).days <= adds:
                            sumRV5 += float(data[j]['rv5'])
                            validDay += 1
                            end = day
                            # print("    ", day)
                    if validDay==0:
                        break
                    row['rv5'] = sumRV5 / validDay * 12
                    
                    row['begin|end'] = str(tagDay).split(' ')[0] + ' to ' + str(end).split(' ')[0] 
                    break
                    
                elif canDay > tagDay:
                    for k in range(i-1, i-6, -1):
                        day = datetime.datetime.strptime(data[k]['date'], "%Y-%m-%d")
                        if (tagDay-day).days <= 5:
                            lastDay = day
                            break;
                    mon = int(str(lastDay).split('-')[1])
                    adds = month[mon]
                    if mon==2:
                        year = int(str(lastDay).split('-')[0])
                        if year==2012 or year==2016 or year==2020:
                            adds += 1   
                    for j in range(k, k+31):
                        if j >= len(data):
                            break
                        day = datetime.datetime.strptime(data[j]['date'], "%Y-%m-%d")
                        if (day-lastDay).days <= adds:
                            sumRV5 += float(data[j]['rv5'])
                            validDay += 1
                            end = day
                    if validDay==0:
                        break 
                    row['rv5'] = sumRV5 / validDay * 12
                    row['begin|end'] = str(lastDay).split(' ')[0] + ' to ' + str(end).split(' ')[0] 
                    break
                else:
                    i += 1
            # print(row)        
            result.append(row)        
            i += 1    
            tagDay = tagDay + datetime.timedelta(days=7)
            
        json2csv(result, sym)
                            
                            
                            
                            
                            
                            
                            
    
