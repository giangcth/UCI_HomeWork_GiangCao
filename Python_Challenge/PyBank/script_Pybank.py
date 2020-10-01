import os
import csv
import numpy as np


PyBank_csv = os.path.join('Pybank','Resources','budget_data.csv')

months = 0
total = 0

lst = []
date = []
changelst = []
change = 0
total_change = 0
averagechange = 0
minchange = 0
maxchange = 0

with open(PyBank_csv, 'r') as csvfile:

    reader = csv.reader(csvfile, delimiter=',')
    header = next(reader)
    
    for row in reader:

        months += 1
        float_month = float(row[1])
        total += float_month
        lst.append(row[1])
        date.append(row[0])

    for i in range(len(lst)-1):
               
        change = int(lst[i+1]) - int(lst[i])

        total_change = total_change + change
        averagechange = total_change / (months - 1)
        changelst.append(change)

        if change > maxchange:
            maxchange = change
            maxindex = changelst.index(maxchange)
            
        elif change < minchange:
            minchange = change
            minindex = changelst.index(minchange)
    
    maxdate = date[maxindex + 1]
    mindate = date[minindex + 1]
    
   
# printing result  

print(f"FINANCIAL ANALYST")
print(f"-----------------------------------------------")
print(f"Total months: " + str(months))
print(f"Total: " + str(total))
print(f"Average Change: " + str(averagechange))
print(f"Greatest Increase in Profits: " + maxdate + " " + str(maxchange))
print(f"Greatest Decrease in Profits: " + mindate + " " + str(minchange))

# the output file

output_PyBank = os.path.join("PyBank.txt")


with open(output_PyBank, "w") as txtfile:
    
    txtfile.write(f"FINANCIAL ANALYST \n")

    L = [(f"------------------------------------------------------------- \n"),
            (f"Total months: " + str(months) + " \n"),
            (f"Total: " + str(total) + " \n"),
            (f"Average Change: " + str(averagechange) + " \n"),
            (f"Greatest Increase in Profits: " + str(maxdate) + " " + str(maxchange) + " \n"),
            (f"Greatest Decrease in Profits: " + str(mindate) + " " + str(minchange) + " \n")]

    txtfile.writelines(L) 
    
    txtfile.close()


    
    


   








    
   