import json
import darkskyreq

def lookupNum(num):
    for x in range(0, len(read())):
        if num in read()[x]['phone']:
            return x

def read():
    with open('userInfo.json', 'r', encoding = 'utf-8') as f:
        return json.load(f)
        
def loadUser(num):
    y = read()[lookupNum(num)]
    u = User(y['first'], y['last'], y['phone'], y['location'], y['time'], y['gender'], y['timezone'])
    return u

def listed(x):
    with open('numbers.json', 'r') as f:
        nums = json.load(f)
    if x not in nums:
        nums.append(x)
        with open ('numbers.json', 'w', encoding = 'utf-8') as f:
            json.dump(nums, f, ensure_ascii=False, indent=4)
            return 1
    
class User:
    def __init__(self, first = '', last = '', phone = '', location = '', time = '', gender = '', timezone = ''):
        self.first = str(first)
        self.last = str(last)
        self.phone = str(phone)
        self.location = str(location)
        self.time = str(time)
        self.gender = str(gender)
        self.timezone = str(timezone)
        
    def writeUser(self):
        with open('userInfo.json', 'r', encoding = 'utf-8') as f:
            data = json.load(f)
        data.append(self.__dict__)
        with open('userInfo.json', 'w', encoding = 'utf-8') as f:
            json.dump(data, f, ensure_ascii = False, indent=4)
            
    def newLoc(self, loc):
        w = darkskyreq.Weather(loc)
        tz = w.getWeather().timezone
        
        self.location = loc
        self.timezone = tz
        u = read()
        for x in range(0, len(u)):
            if self.phone in u[x]['phone']:
                break
        u[x]['location'] = loc
        u[x]['timezone'] = tz
        with open('userInfo.json', 'w', encoding = 'utf-8') as f:
            json.dump(u, f, ensure_ascii = False, indent=4)
            
    def newTime(self, time):
        self.time = time
        u = read()
        for x in range(0, len(u)):
            if self.phone in u[x]['phone']:
                break
        u[x]['time'] = time
        
        with open('userInfo.json', 'w', encoding = 'utf-8') as f:
            json.dump(u, f, ensure_ascii = False, indent=4)
        
        
'''            
data, sheet = sheets.sheetReq()
print (sheets.getLen())
            
for x in range (0, sheets.getLen()):
    first = data[x]['First name']
    last = data[x]['Last Name']
    phone = data[x]['National Format']
    location = data[x]['Your Location (City, state; address; postal code; etc.)']
    time = ''
    gender = data[x]['Gender']
    if phone == '':
        continue
    u1 = User(first, last, phone, location, time, gender)
    u1.writeUser()
'''