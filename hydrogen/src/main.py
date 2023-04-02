from datetime import date, timedelta, datetime, time


class Equipment: 
    def __init__(self, name):
        self.name = name 
        # dictionary with key:value date:[Reservations], holds Reservations from today to 30 days from now
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

    def freet(self, start_date):
        '''
        Returns a list of free time blocks on the date of the given time
        '''
        result = []
        if start_date.weekday() == 6:
            return result 
        elif start_date.weekday() == 5:
            open = datetime.combine(start_date.date(), time(hour=10, minute=0))
            closet = datetime.combine(start_date.date(), time(hour=16, minute=0))
        else:
            open = datetime.combine(start_date.date(), time(hour=9, minute=0))
            closet = datetime.combine(start_date.date(), time(hour=18, minute=0))
        
        if len(self.res[start_date.date()]) == 0:
            result.append([open, closet])
            return result
        
        def helper(r):
            return r.startt
        self.res[start_date.date()].sort(key=helper)

        if self.name == 'scanner':
            # print('current Reservations: ', self.res[start_date.date()])
            for r in self.res[start_date.date()]:
                # print("REServation: ", r.startt, r.end_t)
                if r.startt > open + timedelta(minutes=60):
                    if open != r.startt - timedelta(minutes=60):
                        result.append([open, r.startt - timedelta(minutes=60)])
                    # print(result)
                open = r.end_t + timedelta(minutes=60)
            if open < closet:
                result.append([open, closet])
            return result
        elif self.name == 'scooper':
            for r in self.res[start_date.date()]:
                if r.startt > open:
                    result.append([open, r.startt])
                open = r.end_t
            if open < closet:
                result.append([open, closet])
            return result
        elif self.name == 'harvest':
            for r in self.res[start_date.date()]:
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


    
class Reservation:

    def __init__(self, username, id, Equipment, startt, duration):
        self.username = username
        self.id = id 
        self.Equipment = Equipment
        self.equipn = None
        self.startt = startt
        self.duration = duration
        self.end_t = self.startt + timedelta(minutes=int(duration))
        self.t_cost = 0 
        self.down_p = 0
        self.status = 'pending'
        self.refund = 0

    def __repr__(self):
        return f"Reservation {self.id}: {self.username} booked {self.equipn} for {self.startt} to {self.end_t} for ${self.t_cost}"
    

class Main:
    def __init__(self):
        self.scans = {'1':Equipment('scanner'), '2':Equipment('scanner'), '3':Equipment('scanner'), '4':Equipment('scanner')} 
        self.scoop = {'1':Equipment('scooper'), '2':Equipment('scooper'), '3':Equipment('scooper'), '4':Equipment('scooper')} 
        self.harv = {'1': Equipment('harvest')}
        self.resnum = 0

    def ch_free(self, machine_type, reservation_date):
        # checks for free time blocks
        result = {}
        if machine_type == 'scanner':
            for key, value in self.scans.items():
                result[key] = value.freet(reservation_date)
        elif machine_type == 'scooper':
            for key, value in self.scoop.items():
                result[key] = value.freet(reservation_date)
        elif machine_type == 'harvest':
            for key, value in self.harv.items():
                result[key] = value.freet(reservation_date)
        return result

    def reserve(self, username, machine_type, machine_num, start_time, duration):
        self.resnum += 1
        reservation = Reservation(username, self.resnum, machine_type, start_time, duration)
        time_difference = start_time - datetime.today()
        if machine_type == 'scanner':
            self.scans[machine_num].res[start_time.date()].append(reservation)
            reservation.status = 'booked'
            reservation.equipn = machine_num
            if time_difference.days >= 14:
                reservation.t_cost = .25 * self.scans[machine_num].cost(int(duration) / 60)
                reservation.down_p = 0.5 * reservation.t_cost
            else:
                reservation.t_cost = self.scans[machine_num].cost(int(duration) / 60)
                reservation.down_p = 0.5 * reservation.t_cost
            return reservation
        if machine_type == 'scooper':
            self.scoop[machine_num].res[start_time.date()].append(reservation)
            reservation.status = 'booked'
            reservation.equipn = machine_num
            if time_difference.days >= 14:
                reservation.t_cost = .25 * self.scans[machine_num].cost(int(duration) / 60)
                reservation.down_p = 0.5 * reservation.t_cost
            else:
                reservation.t_cost = self.scans[machine_num].cost(int(duration) / 60)
                reservation.down_p = 0.5 * reservation.t_cost
            return reservation
        if machine_type == 'harvest':
            self.harv[machine_num].res[start_time.date()].append(reservation)
            reservation.status = 'booked'
            reservation.equipn = machine_num
            if time_difference.days >= 14:
                reservation.t_cost = .25 * self.scans[machine_num].cost(int(duration) / 60)
                reservation.down_p = 0.5 * reservation.t_cost
            else:
                reservation.t_cost = self.scans[machine_num].cost(int(duration) / 60)
                reservation.down_p = 0.5 * reservation.t_cost
            return reservation
    
    def cancel(self, machine_type, machine_num, reservation_cancel_date, reservation_id):
        refund = 0
        days_in_advance = 0
        if machine_type == 'scanner':
            # calculate refund
            for reservation in self.scans[machine_num].res[reservation_cancel_date.date()]:
                if reservation.id == int(reservation_id):
                    time_difference = reservation_cancel_date - datetime.today()
                    
                    for i in range(1, time_difference.days+1):
                        day = datetime.today() + timedelta(days=i)
    
                        if day.weekday() < 6:
                            days_in_advance += 1

                    print(f"Cancelled {days_in_advance} days in advance")
                    if days_in_advance >= 2 and days_in_advance < 7:
                        print('50 percent refund')
                        refund = reservation.down_p * 0.5
                    elif days_in_advance >= 7:
                        print('75 percent refund')
                        refund = reservation.down_p * 0.75
                    break
            # print(self.scans[machine_num].res[reservation_cancel_date.date()])
            self.scans[machine_num].res[reservation_cancel_date.date()] = [reservation for reservation in self.scans[machine_num].res[reservation_cancel_date.date()] if reservation.id != int(reservation_id)]
            return refund
            # print(self.scans[machine_num].res[reservation_cancel_date.date()]) 
        elif machine_type == 'scooper':
            # calculate refund
            for reservation in self.scoop[machine_num].res[reservation_cancel_date.date()]:
                if reservation.id == int(reservation_id):
                    time_difference = reservation_cancel_date - datetime.today()
                    for i in range(1, time_difference.days+1):
                        day = datetime.today() + timedelta(days=i)
                        if day.weekday() < 6:
                            days_in_advance += 1
                    print(f"Cancelled {days_in_advance} days in advance")
                    if days_in_advance >= 2 and days_in_advance < 7:
                        print('50 percent refund')
                        refund = reservation.down_p * 0.5
                    elif days_in_advance >= 7:
                        print('75 percent refund')
                        refund = reservation.down_p * 0.75
                    break
            self.scoop[machine_num].res[reservation_cancel_date.date()] = [reservation for reservation in self.scoop[machine_num].res[reservation_cancel_date.date()] if reservation.id != int(reservation_id)]
            return refund
        elif machine_type == 'harvest':
            # calculate refund
            for reservation in self.harv[machine_num].res[reservation_cancel_date.date()]:
                if reservation.id == int(reservation_id):
                    time_difference = reservation_cancel_date - datetime.today()
                    for i in range(1, time_difference.days+1):
                        day = datetime.today() + timedelta(days=i)
                        if day.weekday() < 6:
                            days_in_advance += 1
                    print(f"Cancelled {days_in_advance} days in advance")
                    if days_in_advance >= 2 and days_in_advance < 7:
                        print('50 percent refund')
                        refund = reservation.down_p * 0.5
                    elif days_in_advance >= 7:
                        print('75 percent refund')
                        refund = reservation.down_p * 0.75
                    break
            self.harv[machine_num].res[reservation_cancel_date.date()] = [reservation for reservation in self.harv[machine_num].res[reservation_cancel_date.date()] if reservation.id != int(reservation_id)]
            return refund

    def rbydate(self, start_date, end_date, cust=None, mach=None):
        result = {'scanner':[], 'scooper':[], 'harvest':[]}
        if cust:
            for key, value in self.scans.items():
                for key2, value2 in value.res.items():
                    if key2 >= start_date and key2 <= end_date and len(value2) > 0: 
                        for r in value2:
                            if r.username == cust:
                                result['scanner'].append(r) 
            for key, value in self.scoop.items():
                for key2, value2 in value.res.items():
                    if key2 >= start_date and key2 <= end_date and len(value2) > 0: 
                        for r in value2:
                            if r.username == cust:
                                result['scooper'].append(r) 
            for key, value in self.harv.items():
                for key2, value2 in value.res.items():
                    if key2 >= start_date and key2 <= end_date and len(value2) > 0: 
                        for r in value2:
                            if r.username == cust:
                                result['harvest'].append(r) 
            return result

        for key, value in self.scans.items():
            for key2, value2 in value.res.items():
                if key2 >= start_date and key2 <= end_date and len(value2) > 0: 
                    for r in value2:
                        result['scanner'].append(r) 
        for key, value in self.scoop.items():
            for key2, value2 in value.res.items():
                if key2 >= start_date and key2 <= end_date and len(value2) > 0: 
                    for r in value2:
                        result['scooper'].append(r) 
        for key, value in self.harv.items():
            for key2, value2 in value.res.items():
                if key2 >= start_date and key2 <= end_date and len(value2) > 0: 
                    for r in value2:    
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
        menu_choice = input("Choose a menu item (1 - 6): ")

        if int(menu_choice) == 1:
            print('Reserving a machine')
            while True:
                username = input('Enter username of customer: ')
                machine_type = input('What kind of machine would you like to reserve? (scanner, scooper, harvest): ')
                # get date and return available machines and their open times on that date
                # have user choose machine and time
                reservation_date = datetime.fromisoformat(input(f"Enter desired reservation date (YYYY-MM-DD): "))
                print(system.ch_free(machine_type, reservation_date))
                machine_num = input("Which machine would you like to book? Enter the number: ")
                reservation_time = datetime.fromisoformat(input("What time would you like to book? Choose from free times, on the hour or half hour (YYYY-MM-DDTHH:MM): "))
                duration = input("For how long do you need to book? (enter in minutes, 30 minute increments): ")
                if machine_type == 'scanner' and int(duration) > 120:
                    duration = input("Scanners cannot be reserved for more than 2 hours: ")
                r = system.reserve(username, machine_type, machine_num, reservation_time, duration)
                print(f"Done! Your reservation id is {r.id} for {machine_type} number {machine_num}. That will cost {r.t_cost}, and your down payment is {r.down_p}")
                break 
        elif int(menu_choice) == 2:
            print('Cancel a reservation')
            while True:
                machine_type = input('What kind of machine would you like to cancel? (scanner, scooper, harvest): ')
                machine_num = input(f"Which {machine_type} would you like to cancel?: ")
                reservation_cancel_date = datetime.fromisoformat(input('What was the date and time of your Reservation? (YYYY-MM-DDTHH:MM): '))
                reservation_id = input('What was your reservation id? ')
                refund = system.cancel(machine_type, machine_num, reservation_cancel_date, reservation_id)
                print(f"Done! Your refund is {refund}")
                break
        elif int(menu_choice) == 3:
            print('See reservations by date range')
            while True:
                start_date = date.fromisoformat(input('From (YYYY-MM-DD): '))
                end_date = date.fromisoformat(input('To (YYYY-MM-DD): '))
                print(system.rbydate(start_date, end_date))
                break
        elif int(menu_choice) == 4:
            while True:
                print('See reservations for customer by date range')
                customer_username = input('Customer username: ')
                start_date = date.fromisoformat(input('From (YYYY-MM-DD): '))
                end_date = date.fromisoformat(input('To (YYYY-MM-DD): '))
                print(system.rbydate(start_date, end_date, cust=customer_username))
                break 
        elif int(menu_choice) == 5:
            while True:
                print('See reservations for machine by date range')
                machine_type = input('Machine type (scanner, scooper, harvest): ')
                start_date = date.fromisoformat(input('From (YYYY-MM-DD): '))
                end_date = date.fromisoformat(input('To (YYYY-MM-DD): '))
                print(system.rbydate(start_date, end_date, mach=machine_type))
                break 
        elif int(menu_choice) == 6:
            break



