import numpy as np                                        #call to numpy library

Cvalue=float(input("Please enter a 'C' value: "))    # Get ınput from user  ( "C value" ) 

#---------------DOSYADAN VERİNİN ÇEKİLMESİ---------
data_file= open("veri.txt","r")                           # open text file in read mode
data= [(i.split("\n")[0]) for i in data_file]             # populate list "data" with text file's lines.


numberOfTask=int(data[0])                       # Get "number of task" info 
data.pop(0)                               # Pop the number of task info from "data" list


time={}                                   # Create a dictionary that holds the task time
for i in range((numberOfTask)):
    time[i+1]=(float(data[i]))


prio=[]
for i in range(numberOfTask,len(data)-1):       # Priorities which get from data
    prio.append(data[i])

pr=[(i.split(",")) for i in prio]         #  List the priorities 

#-------ENHANCE THE DATA USABILITY -------
zeros= np.zeros((numberOfTask,numberOfTask))          # Creates a priority matrix of 0s using a numpy array
for n in pr: 
    x=(int(n[0]))-1
    y=(int(n[1]))-1
    zeros[x][y]=1

cleanlist= np.zeros((numberOfTask,1))           # Creates lists as many as  number of task by using np array 
cleanlist=cleanlist.tolist()              #( np array => list ) transformation


for rows in reversed(range(len(zeros))):  # Grouping priorities, starting in reverse
    for el in range(len(zeros[rows])):
        if zeros[rows][el]==1:
            cleanlist[rows].append(el+1)
            

for r in reversed(range(len(cleanlist))): # Grouping priorities, starting in reverse

    cleanlist[r].pop(0)                   # Drop zeros from list(s)
    for elt in cleanlist[r]:              
        
            listforcu=cleanlist[elt-1]
            cleanlist[r]=(cleanlist[r])+(listforcu)  # Creating lists cumulatively from bottom to top
            
    cleanlist[r].insert(0,r+1)                        # Inclusion of tasks' own numbers in the list
lenght=len(cleanlist)
cleanlist[lenght-1].insert(0,lenght)       # Addition of the last element to the last set
    
     
def duplicate(x):                          # Defining a function to delete repetitive tasks in the list and leave 1 each ( using dictionary) 
  return list(dict.fromkeys(x))    


caltlist = cleanlist.copy()                # A copy of the cleanlist list is created for calculations
caltlist = list(map(duplicate,caltlist))   # Repetitive tasks in the list are deleted

copytime= time.copy()                      # The dictionary where the times are kept is copied
 
for ls in range(len(caltlist)):            # Matching corresponding times in the time dictionary By navigating over the values in the calculation list one by one     
      for p in range(len(caltlist[ls])):        
           caltlist[ls][p]=copytime[caltlist[ls][p]]

total= list(map(sum,caltlist))             # Calculation of task weights by collecting the data in the calculation list
                        

weight_dict={}                             # Creating the dictionary where the weight data is kept according to the task
for item in range(len(total)):            
    weight_dict[(item+1)]=total[item]

sorted_dict = sorted(weight_dict.items(), key=(lambda x: x[1]), reverse=True)    # sorting the task weights from largest to smallest
 

#--------------ASSIGNMENT TO STATIONS ----------------
# Defining variables, lists and dictionaries

remain= Cvalue                             # Taking the C value to calculate the idle time at the station
Remain_Container={}                          # Dictionary to keep station idle times

Stations={}                                # Dictionary to keep station assignments

stationNo=1                                
Stations[stationNo]=[]                     # Opening of the first station

row=0

while row < len(sorted_dict):                 
    timeofitem=time[sorted_dict[row][0]]                    # Duration of the task
    remain= remain - timeofitem
    if remain >= 0:                                         # Station remaining time control
        Stations[stationNo].append(sorted_dict[row][0])
        Remain_Container[stationNo]=remain
        row+=1 #görevin istasyona eklenmesi  
    else:
        stationNo+=1
        Stations[stationNo]=[]
        remain = Cvalue


       
#----------------Performance Calculations -----------
Station_Total={}                                           # create a dictionary to hold Durations by Station 

for i in range(len(Remain_Container)):
    Station_Total[i+1]= Cvalue - Remain_Container[i+1]

#--------------BALANCE DELAY ---------------------
balanceDelaySum = sum(Station_Total.values())                  # Total Station Time

balanceDelay=(((len(Station_Total))*Cvalue)-balanceDelaySum)/((len(Station_Total))*Cvalue)  # Calculation of balance delay


#--------------Line Efficiency---------------
lineEfficiency = balanceDelaySum/((len(Station_Total))*Cvalue)    # Line Efficiency calculation


#--------------Line Smoothness Index--------------
smoothnessSum=[]                                           # Line Smoothness Index Calculation
MaxSTVal=max(Station_Total.values())

for  k in Station_Total:
        res=((MaxSTVal)-Station_Total[k])**2
        smoothnessSum.append(res)
totalSmoothness=sum(smoothnessSum)
SI=totalSmoothness**(1/2)
SIPercent= SI/(Cvalue*(len(Station_Total)))

totalIdle= sum(Remain_Container.values())

#--------------PRINT THE RESULTS ON SCREEN PART-------------- 
print("\n")
print("* * * - - - - - - - - - - - - - - - - - RESULTS - - - - - - - - - - - - - - - - - * * *")

print("Assigned element number:",numberOfTask,"\n" )
print("Total Station Number:", len(Station_Total),"\n")
print("Total Station Idle Time:",totalIdle)

print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
for k in Stations:
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ")
    text="{StName}. Station :{StTask} // Station Time: {StTime} // Station Idle Time: {StIDLE}"
    print(text.format(StName=k,StTask=Stations[k],StTime=Station_Total[k],StIDLE=Remain_Container[k]))
    

print("- - - - - - - - - - - -")
print("Balance Delay Value:","%",round(balanceDelay*100,4))
print("* * * * * * ")
print("Line Efficiency Value:","%",round(lineEfficiency*100,4))
print("* * * * * * ")
print("Line Smoothness Index:",round(SI,4))
              
