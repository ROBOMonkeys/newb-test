def vacation_trips(airplane_rides):
    if 2500.00 > airplane_rides:
        print ("Canada")
    elif 2500.01 < airplane_rides and airplane_rides < 5000.00:
        print ("Hawaii")
    elif 5000.01 < airplane_rides < 10000.00:
        print ("Rome")
    else:
        print ("Japan")

rides = input("what is your budget ")
vacation_trips(float(rides))