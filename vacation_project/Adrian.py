def location(budget):
    if 2500.00 > budget:
        print("Canada")
    elif 2500.01 < budget < 5000.00:
        print("Hawaii")
    elif 5000.01 < budget < 10000.00:
        print("Rome")
    else:
        print("Russia")

budget = input("Enter your budget")
location(float(budget))