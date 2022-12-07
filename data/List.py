# Get a list of S&P500 's `Symbol`
import array
import csv

#url = 'Stocks in the SP 500 Index.csv'
symbol_list = list()
sector_set = set()

def Category_list(url):
    with open(url, newline='') as csvfile:
        reader = csv.DictReader(csvfile , delimiter=',')
        for row in reader:
            symbol = row['Symbol']
            sector = row['GICS Sector']
            symbol_list.append(symbol)
            sector_set.add(sector)
    return symbol_list, sector_set

Category_list('Stocks in the SP 500 Index.csv')

with open('SP500symbols.csv', 'a') as f: 
    write = csv.writer(f) 
    write.writerow(symbol_list)
with open('SP500sectors.csv', 'a') as f: 
    write = csv.writer(f) 
    write.writerow(sector_set)
    
