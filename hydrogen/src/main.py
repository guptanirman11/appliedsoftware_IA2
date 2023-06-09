from datetime import date, timedelta, datetime, time
import copy

class Equipment: 
    def __init__(self, name):
        self.name = name 
        # dictionary with key:value date:[Reservations], holds Reservations from today to 30 days from now
        self.res = {}
        for i in range(0, 31):
            newdate = datetime.now() + timedelta(days = i)
            self.res[newdate.date()] = []
    
    def cost(self, hours):
        # Calculate the cost of using the equipment for a given number of hours
        
        if self.name == 'scanner':
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
        # Check if the start_date is on a Sunday, if so return an empty list
        if start_date.weekday() == 6:
            return result 
         # Check if the start_date is on a Saturday, if so set the opening and closing times accordingly
        elif start_date.weekday() == 5:
            open = datetime.combine(start_date.date(), time(hour=10, minute=0))
            closet = datetime.combine(start_date.date(), time(hour=16, minute=0))
        # For all other days, set the opening and closing times accordingly
        else:
            open = datetime.combine(start_date.date(), time(hour=9, minute=0))
            closet = datetime.combine(start_date.date(), time(hour=18, minute=0))
        
        # If there are no reservations for the given date, return the entire time block as free
        if len(self.res[start_date.date()]) == 0:
            result.append([open, closet])
            return result
        
        '''Helper function  Sort the reservations for the given date in chronological order.'''
        def helper(r):
            return r.startt
        
        self.res[start_date.date()].sort(key=helper)

        # Check for free time blocks between reservations for a scanner, scooper and harvester
       
        for r in self.res[start_date.date()]:
            # print("REServation: ", r.startt, r.end_t)
            if r.startt > open + timedelta(minutes=60):
                if open != r.startt - timedelta(minutes=60):
                    result.append([open, r.startt - timedelta(minutes=60)])
                # print(result)
            open = r.end_t + timedelta(minutes=60)

        # Check for free time after the last reservation, if any
        if open < closet:
            result.append([open, closet])
        return result


'''Reservation class with username, id, Equipment name , start time and duration as class variables'''
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

    '''Initialising the scanners, scoopers and harvster dictionaries'''
    def __init__(self):
        self.scans = {'1':Equipment('scanner'), '2':Equipment('scanner'), '3':Equipment('scanner'), '4':Equipment('scanner')} 
        self.scoop = {'1':Equipment('scooper'), '2':Equipment('scooper'), '3':Equipment('scooper'), '4':Equipment('scooper')} 
        self.harv = {'1': Equipment('harvest')}
        self.resnum = 0
    '''
    Check free time blocks for each machine(scanner/scooper/harvester) on a particular date.
    returns a dictionary with key as machine number and values as available time blocks. '''
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
    '''
    takes username/company name, machine type, machine number, start_time and duration (in minutes) as input
    output: retuns reservation information and ereserves the particular machine within the given time slot.'''
    def reserve(self, username, machine_type, machine_num, start_time, duration):
        self.resnum += 1
        reservation = Reservation(username, self.resnum, machine_type, start_time, duration)
        time_difference = start_time - datetime.today()
        
        if machine_type == 'scanner':
            
            #Loop to check if the slot is already booked or not for specific machine
            for res in self.scans[machine_num].res[start_time.date()]: 
                if res.startt <= start_time and start_time + timedelta(minutes=int(duration)) <=res.end_t : 
                    print("already booked time slot")
                    return
            
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
            for res in self.scoop[machine_num].res[start_time.date()]:
                
                if res.startt <= start_time and start_time + timedelta(minutes=int(duration)) <=res.end_t : 
                    print("already booked time slot")
                    return
            self.scoop[machine_num].res[start_time.date()].append(reservation)
            reservation.status = 'booked'
            reservation.equipn = machine_num
            if time_difference.days >= 14:
                reservation.t_cost = .25 * self.scoop[machine_num].cost(int(duration) / 60)
                reservation.down_p = 0.5 * reservation.t_cost
            else:
                reservation.t_cost = self.scoop[machine_num].cost(int(duration) / 60)
                reservation.down_p = 0.5 * reservation.t_cost
            return reservation
        
        if machine_type == 'harvest':
            for res in self.harv[machine_num].res[start_time.date()]:
                
                if res.startt <= start_time and start_time + timedelta(minutes=int(duration)) <=res.end_t : 
                    print("already booked time slot")
                    return
            self.harv[machine_num].res[start_time.date()].append(reservation)
            reservation.status = 'booked'
            reservation.equipn = machine_num
            if time_difference.days >= 14:
                reservation.t_cost = .25 * self.harv[machine_num].cost(int(duration) / 60)
                reservation.down_p = 0.5 * reservation.t_cost
            else:
                reservation.t_cost = self.harv[machine_num].cost(int(duration) / 60)
                reservation.down_p = 0.5 * reservation.t_cost
            return reservation
    '''
    method of main class which takes input machine type(scooper/scanner/harvester), machine number(1/2/3/4) , reservation_cancel_date, and reservation id '''
    def cancel(self, machine_type, machine_num, reservation_cancel_date, reservation_id):
        #variables local to method 
        refund = 0
        days_in_advance = 0
        '''  calculate refund depending upon the machine type
        takes a copy of the reservation list depending upon the equipment
        calculates the refund
        remove the reservation from the list
        returns the refund'''

        if machine_type == "scanner":
            machine_reservations = self.scans[machine_num].res[reservation_cancel_date.date()]
        elif machine_type == "scooper":
            machine_reservations = self.scoop[machine_num].res[reservation_cancel_date.date()]
        elif machine_type == "harvest":
            machine_reservations = self.harv[machine_num].res[reservation_cancel_date.date()]

        for reservation in machine_reservations:
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
        if machine_type == "scanner":
            self.scans[machine_num].res[reservation_cancel_date.date()] = [reservation for reservation in self.scans[machine_num].res[reservation_cancel_date.date()] if reservation.id != int(reservation_id)]
        elif machine_type == "scooper":
            self.scoop[machine_num].res[reservation_cancel_date.date()] = [reservation for reservation in self.scoop[machine_num].res[reservation_cancel_date.date()] if reservation.id != int(reservation_id)]
        elif machine_type == "harvest":
            self.harv[machine_num].res[reservation_cancel_date.date()] = [reservation for reservation in self.harv[machine_num].res[reservation_cancel_date.date()] if reservation.id != int(reservation_id)]
        
        return refund
    
    '''Input:Function takes start date, end date, customer and machine name if required and
     returns dictionary of list of reservation within that date range of each machine type unless mantioned.'''
    def rbydate(self, start_date, end_date, customer=None, machine=None):
        #maintining a dictionary of scanners, scoopers and harvesters which will contain the reservations within the date range.
        result = {'scanner':[], 'scooper':[], 'harvest':[]}
        # if customer:
        for key, value in self.scans.items():
            for key2, value2 in value.res.items():
                if key2 >= start_date and key2 <= end_date and len(value2) > 0: 
                    for r in value2:
                        if customer:
                            if r.username == customer:
                                result['scanner'].append(r)
                        else:
                                result['scanner'].append(r)
        for key, value in self.scoop.items():
            for key2, value2 in value.res.items():
                if key2 >= start_date and key2 <= end_date and len(value2) > 0: 
                    for r in value2:
                        if customer:
                            if r.username == customer:
                                result['scooper'].append(r)
                        else:
                                result['scooper'].append(r)
        for key, value in self.harv.items():
            for key2, value2 in value.res.items():
                if key2 >= start_date and key2 <= end_date and len(value2) > 0: 
                    for r in value2:
                        if customer:
                            if r.username == customer:
                                result['harvest'].append(r)
                        else:
                                result['harvest'].append(r)

        if machine:
            return result[machine]
        else:              
            return result


while True:
    system = Main()
    print('Welcome! Press enter to continue or type exit to leave')

    if input() == 'exit':
        break
    ''' The main loop which displays the that displays the menu options and prompts the user to choose an action '''
    
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
                
                #Check to make sure that scanners are not booked for no more than 2 hours because of the constraints.
                if machine_type == 'scanner' and int(duration) > 120:
                    duration = input("Scanners cannot be reserved for more than 2 hours: ")
                
                r = system.reserve(username, machine_type, machine_num, reservation_time, duration)
                if r != None:
                    print(f"Done! Your reservation id is {r.id} for {machine_type} number {machine_num}. That will cost {r.t_cost}, and your down payment is {r.down_p}")
                break 
        
        elif int(menu_choice) == 2:
            print('Cancel a reservation')
            while True:
                machine_type = input('What kind of machine would you like to cancel? (scanner, scooper, harvest): ')
                machine_num = input(f"Which {machine_type} would you like to cancel?: ")
                reservation_cancel_date = datetime.fromisoformat(input('What was the date and time of your Reservation? (YYYY-MM-DDTHH:MM): '))
                reservation_id = input('What was your reservation id? ')
                
                #Calculating the refund using cancel method defined in main class which updates the list of reservations as well.
                refund = system.cancel(machine_type, machine_num, reservation_cancel_date, reservation_id)

                print(f"Done! Your refund is {refund}")
                break
        
        
        elif int(menu_choice) == 3:
            print('See reservations by date range')
            while True:
                start_date = date.fromisoformat(input('From (YYYY-MM-DD): '))
                end_date = date.fromisoformat(input('To (YYYY-MM-DD): '))
                
                #returns list of reservations within the given date range using rbydate method of main class.
                print(system.rbydate(start_date, end_date))
                break
        
        elif int(menu_choice) == 4:
            while True:
                print('See reservations for customer by date range')
                customer_username = input('Customer username: ')
                start_date = date.fromisoformat(input('From (YYYY-MM-DD): '))
                end_date = date.fromisoformat(input('To (YYYY-MM-DD): '))

                #returns list of reservations of a given customer within the given date range using rbydate method of main class.
                print(system.rbydate(start_date, end_date, customer=customer_username))
                break 
        elif int(menu_choice) == 5:
            while True:
                print('See reservations for machine by date range')
                machine_type = input('Machine type (scanner, scooper, harvest): ')
                start_date = date.fromisoformat(input('From (YYYY-MM-DD): '))
                end_date = date.fromisoformat(input('To (YYYY-MM-DD): '))

                #returns list of reservations of a particular machine within the given date range using rbydate method of main class.
                print(system.rbydate(start_date, end_date, machine = machine_type))
                break 
        elif int(menu_choice) == 6:
            break