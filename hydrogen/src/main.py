from datetime import date, timedelta, datetime, time


class Equip: 
    def __init__(self, name):
        self.name = name 
        # dictionary with key:value date:[Resys], holds Resys from today to 30 days from now
        self.res = {}
        for i in range(0, 31):
            newdate = datetime.now() + timedelta(days = i)
            self.res[newdate.date()] = []
    
    def cost(self, hours):
        if self.name == 'scanner':
            # if the equipment is a scanner
            return 990 * hours 
        elif self.name == 'scooper':
            return 1000 * hours 
        elif self.name == 'harvest':
            return 88000

    def freet(self, s_time):
        '''
        Returns a list of free time blocks on the date of the given time
        '''
        result = []
        if s_time.weekday() == 6:
            return result 
        elif s_time.weekday() == 5:
            open = datetime.combine(s_time.date(), time(hour=10, minute=0))
            closet = datetime.combine(s_time.date(), time(hour=16, minute=0))
        else:
            open = datetime.combine(s_time.date(), time(hour=9, minute=0))
            closet = datetime.combine(s_time.date(), time(hour=18, minute=0))
        
        if len(self.res[s_time.date()]) == 0:
            result.append([open, closet])
            return result
        
        def helper(r):
            return r.startt
        self.res[s_time.date()].sort(key=helper)

        if self.name == 'scanner':
            # print('current Resys: ', self.res[s_time.date()])
            for r in self.res[s_time.date()]:
                # print("RESY: ", r.startt, r.end_t)
                if r.startt > open + timedelta(minutes=60):
                    if open != r.startt - timedelta(minutes=60):
                        result.append([open, r.startt - timedelta(minutes=60)])
                    # print(result)
                open = r.end_t + timedelta(minutes=60)
            if open < closet:
                result.append([open, closet])
            return result
        elif self.name == 'scooper':
            for r in self.res[s_time.date()]:
                if r.startt > open:
                    result.append([open, r.startt])
                open = r.end_t
            if open < closet:
                result.append([open, closet])
            return result
        elif self.name == 'harvest':
            for r in self.res[s_time.date()]:
                if r.startt > open + timedelta(hours=6):
                    if open != r.startt - timedelta(hours=6):
                        result.append([open, r.startt - timedelta(hours=6)])
                open = r.end_t + timedelta(hours=6)
            if open < closet:
                result.append([open, closet])
            return result


    def avail(self, startt):
            free = self.freet(startt)
            for f in free: 
                if startt > f[0] and startt < f[1]:
                    return True 
            return False


    
class Resy:

    def __init__(self, usern, id, Equip, startt, durat):
        self.usern = usern
        self.id = id 
        self.Equip = Equip
        self.equipn = None
        self.startt = startt
        self.durat = durat
        self.end_t = self.startt + timedelta(minutes=int(durat))
        self.t_cost = 0 
        self.down_p = 0
        self.status = 'pending'
        self.refund = 0

    def __repr__(self):
        return f"Resy {self.id}: {self.usern} booked {self.equipn} for {self.startt} to {self.end_t} for ${self.t_cost}"
    

class Main:
    def __init__(self):
        self.scans = {'1':Equip('scanner'), '2':Equip('scanner'), '3':Equip('scanner'), '4':Equip('scanner')} 
        self.scoop = {'1':Equip('scooper'), '2':Equip('scooper'), '3':Equip('scooper'), '4':Equip('scooper')} 
        self.harv = {'1': Equip('harvest')}
        self.resnum = 0

    def ch_free(self, m_type, r_dt):
        # checks for free time blocks
        result = {}
        if m_type == 'scanner':
            for k, v in self.scans.items():
                result[k] = v.freet(r_dt)
        elif m_type == 'scooper':
            for k, v in self.scoop.items():
                result[k] = v.freet(r_dt)
        elif m_type == 'harvest':
            for k, v in self.harv.items():
                result[k] = v.freet(r_dt)
        return result

    def reserve(self, usern, m_type, m_num, s_time, durat):
        self.resnum += 1
        r = Resy(usern, self.resnum, m_type, s_time, durat)
        td = s_time - datetime.today()
        if m_type == 'scanner':
            self.scans[m_num].res[s_time.date()].append(r)
            r.status = 'booked'
            r.equipn = m_num
            if td.days >= 14:
                r.t_cost = .25 * self.scans[m_num].cost(int(durat) / 60)
                r.down_p = 0.5 * r.t_cost
            else:
                r.t_cost = self.scans[m_num].cost(int(durat) / 60)
                r.down_p = 0.5 * r.t_cost
            return r
        if m_type == 'scooper':
            self.scoop[m_num].res[s_time.date()].append(r)
            r.status = 'booked'
            r.equipn = m_num
            if td.days >= 14:
                r.t_cost = .25 * self.scans[m_num].cost(int(durat) / 60)
                r.down_p = 0.5 * r.t_cost
            else:
                r.t_cost = self.scans[m_num].cost(int(durat) / 60)
                r.down_p = 0.5 * r.t_cost
            return r
        if m_type == 'harvest':
            self.harv[m_num].res[s_time.date()].append(r)
            r.status = 'booked'
            r.equipn = m_num
            if td.days >= 14:
                r.t_cost = .25 * self.scans[m_num].cost(int(durat) / 60)
                r.down_p = 0.5 * r.t_cost
            else:
                r.t_cost = self.scans[m_num].cost(int(durat) / 60)
                r.down_p = 0.5 * r.t_cost
            return r
    
    def cancel(self, m_type, m_num, r_dt, r_id):
        refund = 0
        ds = 0
        if m_type == 'scanner':
            # calculate refund
            for r in self.scans[m_num].res[r_dt.date()]:
                if r.id == int(r_id):
                    td = r_dt - datetime.today()
                    for i in range(1, td.days+1):
                        d = datetime.today() + timedelta(days=i)
                        if d.weekday() < 6:
                            ds += 1
                    print(f"Cancelled {ds} days in advance")
                    if ds >= 2 and ds < 7:
                        print('50 percent refund')
                        refund = r.down_p * 0.5
                    elif ds >= 7:
                        print('75 percent refund')
                        refund = r.down_p * 0.75
                    break
            # print(self.scans[m_num].res[r_dt.date()])
            self.scans[m_num].res[r_dt.date()] = [r for r in self.scans[m_num].res[r_dt.date()] if r.id != int(r_id)]
            return refund
            # print(self.scans[m_num].res[r_dt.date()]) 
        elif m_type == 'scooper':
            # calculate refund
            for r in self.scoop[m_num].res[r_dt.date()]:
                if r.id == int(r_id):
                    td = r_dt - datetime.today()
                    for i in range(1, td.days+1):
                        d = datetime.today() + timedelta(days=i)
                        if d.weekday() < 6:
                            ds += 1
                    print(f"Cancelled {ds} days in advance")
                    if ds >= 2 and ds < 7:
                        print('50 percent refund')
                        refund = r.down_p * 0.5
                    elif ds >= 7:
                        print('75 percent refund')
                        refund = r.down_p * 0.75
                    break
            self.scoop[m_num].res[r_dt.date()] = [r for r in self.scoop[m_num].res[r_dt.date()] if r.id != int(r_id)]
            return refund
        elif m_type == 'harvest':
            # calculate refund
            for r in self.harv[m_num].res[r_dt.date()]:
                if r.id == int(r_id):
                    td = r_dt - datetime.today()
                    for i in range(1, td.days+1):
                        d = datetime.today() + timedelta(days=i)
                        if d.weekday() < 6:
                            ds += 1
                    print(f"Cancelled {ds} days in advance")
                    if ds >= 2 and ds < 7:
                        print('50 percent refund')
                        refund = r.down_p * 0.5
                    elif ds >= 7:
                        print('75 percent refund')
                        refund = r.down_p * 0.75
                    break
            self.harv[m_num].res[r_dt.date()] = [r for r in self.harv[m_num].res[r_dt.date()] if r.id != int(r_id)]
            return refund

    def rbydate(self, start, end, cust=None, mach=None):
        result = {'scanner':[], 'scooper':[], 'harvest':[]}
        if cust:
            for k, v in self.scans.items():
                for k2, v2 in v.res.items():
                    if k2 >= start and k2 <= end and len(v2) > 0: 
                        for r in v2:
                            if r.usern == cust:
                                result['scanner'].append(r) 
            for k, v in self.scoop.items():
                for k2, v2 in v.res.items():
                    if k2 >= start and k2 <= end and len(v2) > 0: 
                        for r in v2:
                            if r.usern == cust:
                                result['scooper'].append(r) 
            for k, v in self.harv.items():
                for k2, v2 in v.res.items():
                    if k2 >= start and k2 <= end and len(v2) > 0: 
                        for r in v2:
                            if r.usern == cust:
                                result['harvest'].append(r) 
            return result

        for k, v in self.scans.items():
            for k2, v2 in v.res.items():
                if k2 >= start and k2 <= end and len(v2) > 0: 
                    for r in v2:
                        result['scanner'].append(r) 
        for k, v in self.scoop.items():
            for k2, v2 in v.res.items():
                if k2 >= start and k2 <= end and len(v2) > 0: 
                    for r in v2:
                        result['scooper'].append(r) 
        for k, v in self.harv.items():
            for k2, v2 in v.res.items():
                if k2 >= start and k2 <= end and len(v2) > 0: 
                    for r in v2:    
                        result['harvest'].append(r) 
        if mach:
            return result[mach]
        else:              
            return result


while True:
    system = Main()
    print('Welcome! Press enter to continue or type exit to leave')

    if input() == 'exit':
        break

    while True:
        menu = 'Menu:\n 1. Reserve a Machine\n 2. Cancel a Reservation\n 3. See Reservations by Date Range\n '\
            '4. See Reservations for cust by Date Range\n 5. See Reservations for Machine by Date Range\n 6. Log Out'
        print(menu)
        mc = input("Choose a menu item (1 - 6): ")

        if int(mc) == 1:
            print('Reserving a machine')
            while True:
                usern = input('Enter username of customer: ')
                m_type = input('What kind of machine would you like to reserve? (scanner, scooper, harvest): ')
                # get date and return available machines and their open times on that date
                # have user choose machine and time
                r_date = datetime.fromisoformat(input(f"Enter desired reservation date (YYYY-MM-DD): "))
                print(system.ch_free(m_type, r_date))
                m_num = input("Which machine would you like to book? Enter the number: ")
                r_time = datetime.fromisoformat(input("What time would you like to book? Choose from free times, on the hour or half hour (YYYY-MM-DDTHH:MM): "))
                durat = input("For how long do you need to book? (in minutes, 30 minute increments): ")
                if m_type == 'scanner' and int(durat) > 120:
                    durat = input("Scanners cannot be reserved for more than 2 hours: ")
                r = system.reserve(usern, m_type, m_num, r_time, durat)
                print(f"Done! Your reservation id is {r.id} for {m_type} number {m_num}. That will cost {r.t_cost}, and your down payment is {r.down_p}")
                break 
        elif int(mc) == 2:
            print('Cancel a reservation')
            while True:
                m_type = input('What kind of machine would you like to cancel? (scanner, scooper, harvest): ')
                m_num = input(f"Which {m_type} would you like to cancel?: ")
                r_dt = datetime.fromisoformat(input('What was the date and time of your Resy? (YYYY-MM-DDTHH:MM): '))
                r_id = input('What was your reservation id? ')
                refund = system.cancel(m_type, m_num, r_dt, r_id)
                print(f"Done! Your refund is {refund}")
                break
        elif int(mc) == 3:
            print('See reservations by date range')
            while True:
                start = date.fromisoformat(input('From (YYYY-MM-DD): '))
                end = date.fromisoformat(input('To (YYYY-MM-DD): '))
                print(system.rbydate(start, end))
                break
        elif int(mc) == 4:
            while True:
                print('See reservations for customer by date range')
                cust = input('Customer username: ')
                start = date.fromisoformat(input('From (YYYY-MM-DD): '))
                end = date.fromisoformat(input('To (YYYY-MM-DD): '))
                print(system.rbydate(start, end, cust=cust))
                break 
        elif int(mc) == 5:
            while True:
                print('See reservations for machine by date range')
                machine = input('Machine type (scanner, scooper, harvest): ')
                start = date.fromisoformat(input('From (YYYY-MM-DD): '))
                end = date.fromisoformat(input('To (YYYY-MM-DD): '))
                print(system.rbydate(start, end, mach=machine))
                break 
        elif int(mc) == 6:
            break


