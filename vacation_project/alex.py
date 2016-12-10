money=input ("put money")

def vacation(x):
    if 2500.01 > x:
        print ("canada")
    elif 2500.01 < x  < 5000.01:
        print("hawaii")
    elif 5000.01 < x < 10000.00:
        print("rome")
    else:
        print ("mexico")
vacation (float(money))