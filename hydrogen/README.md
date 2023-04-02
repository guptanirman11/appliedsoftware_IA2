## How to run
- From your terminal, run the following: 'python3 <path to project folder>/IA-01/src/main.py'
- Follow the instructions to press Enter to continue or type 'exit' to leave
- Follow the instructions to select the menu item of your choice and enter in the appropriate input

## Assumptions / Simplifications
- Machine usage assumptions
-- The program assumes that the operator has discussed the speed at which the equipment works with the customer to calculate the appropriate duration of a reservation (e.g. they will book a scanner for 30 minutes if the customer needs to scan one (1) block).
-- For an ore scooper, the program assumes that the customer will empty the scooper at a collection drum located at one of the four corners of the grid, so the operator will consult with the cust to determine the appropriate durat to rent a scooper. 
-- The system assumes that the operator will consult with the customer to bake in the time needed to return the Equip (i.e. travel time from where the work is being done to the rental station) to the duration of the reservation. 
- Operator usage assumptions
-- The program assumes that the system user (operator) correctly follows formatting instruction and inputs sensical text. There are minimal guardrails, and the system may crash if the user does not enter correctly formatted and sensical data.
-- The program assumes that the operator will select times that are within operating hours and dates that are currently available (within 30 days and not in the past). Otherwise, the system will crash.
-- The program assumes that the operator will book in 30 minute increments. There are no guardrails to prevent other cases. 
-- When cancelling a reservation, the program assumes that the operator will know the type of machine, machine number, exact datetime, and reservation id of the reservation.
- System assumptions
-- The program assumes that it will always be on. Once it is turned off (user exits in the terminal), all data will be wiped. 
- Reservation assumptions
-- When calculating days for reservations, the program includes weekends in its count (e.g. making reservations 30 days in advance and reserving at least two weeks in advnace include Saturdays and Sundays in the count)
-- However, refunds for cancellations are calculated using business days (Mon - Sat).

## Bugs
- To reiterate what was stated above, due to the assumptions made and the guideline to avoid exception handling, entering incorrect data or data that do not exist (e.g. reservations) will crash the system. 

## Code Smells
- Commenting
-- Functions and classes are not consistently commented. The ones that are commented are either under-commented, or commented due to poor and unclear variable naming. For example, a comment in the cost method in the Eqip class just repeats the code, and a comment for ch_free method in the Main class is necessary because the method name is unclear.
- Switch statements and duplicate code
-- There are several blocks of code with multiple if statements that involve nearly identifcal code. For example, Equip class to represent all equipment includes unnecessary switch statements and duplicate code to handle logic based on whether the piece of equipment is a scanner, scooper, or harvest. This should likely be an abstract base class that subclasses representing the different equipment would inherit. 
- Tight coupling
-- Classes were generally poorly designed with little consideration for responsibility and ended up being tightly coupled and accessing each other's attributes. For example, the reserve method in the Main class updates the status and equipn (equipment number) attributes of the Resy object directly, after being tightly coupled to the name of the Resy class. If the name of that class changes, then the Main class will fail. 

## Grading
- I am not attempting to earn an E
