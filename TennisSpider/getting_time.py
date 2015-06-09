import time

def get_time():
    '''
    '''
    t = time.localtime(time.time())
    year = t.tm_year
    month = t.tm_mon
    day = t.tm_mday
    return ((year, month, day))

def make_data(year, month, day):
    '''
    '''
    new_year = str(year)
    if  day < 10:
        new_day = '0' + str(day)
    else:
        new_day = str(day)
    if month < 10:
        new_month = '0' + str(month)
    else:
        new_month = str(month)
    string = new_year + '-' + new_month + '-' + new_day  
    return string

#Getting new data
def is_leap(year):
    '''
    '''
    if ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0):
        return True
    else:
        return False

def koldays(m, y):
    '''
    '''
    month_31 = [1, 3, 5, 7, 8, 10, 12]
    month_30 = [4, 6, 9, 11]
    if m in month_31:
        return 31;
    elif m in month_30:
        return 30;
    elif m == 2:
        if is_leap(y):
            return 29
        else:
            return 28

def nextday(d, m, y, backi):
    '''
    '''
    if (1 <= d + 1*backi) and (d + 1*backi <= koldays(m, y)):
        d = d + 1*backi
    else:
        if (1 <= m + 1*backi) and (m + 1*backi <= 12):
            m = m + 1*backi;
            d = 1 if backi == 1 else koldays(m, y)
        else:
            d = 1 if backi == 1 else koldays(12, y)
            m = 1 if backi == 1 else 12
            y = y + 1*backi
    return d, m, y

def get_data(day, month, year, n):
    '''
    '''
    backi = 1 if n > 0 else -1
    i = 0
    while abs(i) < abs(n):
        (day, month, year) = nextday(day, month, year, backi)
        i += 1*backi
    return make_data(year, month, day)
