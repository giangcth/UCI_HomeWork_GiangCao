import os
import csv
import sys



PyPoll_csv = os.path.join('Pypoll','Resources','election_data.csv')

totalvoters = 0
count = 0
percent = 0

candidates = []
countcandidate = []
percentcandidate = []

with open(PyPoll_csv, 'r') as csvfile:

    reader = csv.reader(csvfile, delimiter=',')
    header = next(reader)
    
    for row in reader:
        totalvoters +=1
        if row[2] not in candidates:
           candidates.append(row[2])
    
    
    for i in candidates:
        count = 0
        percent = 0
        
        csvfile.seek(0)
        next(reader)

        for row in reader:
            if i == row[2]:
                
                count += 1
                percent = round((count / totalvoters) * 100)
                    
        countcandidate.append(count)
        percentcandidate.append(percent)

roster=zip(candidates, percentcandidate, countcandidate)
roster2=zip(candidates, percentcandidate, countcandidate)

maxpercent = max(percentcandidate)
winnerindex =percentcandidate.index(maxpercent)
winner = candidates[winnerindex]

#print result

print(f"ELECTION RESULTS")
print(f"-----------------------------------------------")

for c, p, o in roster:
    print(f'{c} : {p} % ({o})')

print(f"-----------------------------------------------")

print("The Winner: " + winner)
print(f"-----------------------------------------------")


# Write the output file

output_PyBank = os.path.join("PyPoll.txt")

with open(output_PyBank, "w") as txtfile:

    txtfile.write(f"ELECTION RESULTS \n")
    txtfile.write(f"------------------------------------------------------------- \n")
    txtfile.write("Total Votes: " + str(totalvoters) + " \n")
    
    for c, p, o in roster2:
        txtfile.write(f'{c} : {p} % ({o}) \n')
    
    txtfile.write(f"------------------------------------------------------------- \n")
    
    txtfile.write("The Winner: " + str(winner)+ " \n")
    
    txtfile.write(f"------------------------------------------------------------- \n")


   

 						
						


 











