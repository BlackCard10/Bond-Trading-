import csv
import numpy as np

reader = csv.reader(open('newData.csv','rU'))

bondDictionary = {}
for row in reader:
	key = row[0]
	bondDictionary[key]= row[1:]



# Markov transition matrix given five states/grades of a loan: A, B, C, D, E.  D is a state
# of current default and E is a state of having previously been in the default state D.  

def transitionMatrix(): 					
	R = [.970, .020, .010, .000, .000]
	S = [.050, .800, .150, .000, .000]
	T = [.010, .020, .750, .220, .000]	 
	Y = [.000, .000, .000, .000, 1.000]
	Z = [.000, .000, .000, .000, 1.000]
	
	x = np.matrix( ((R), (S), (T), (Y), (Z)) ) 
	
	return x
	 
# Calculates transition matrix ^ (years)
def matrixPower(years): 
	return transitionMatrix()** years
	
# Length of the bond in years	
def bondRating(ID): 
	ID = str(ID)
	List = bondDictionary[ID]
	Rating = List[1]
	return Rating 

# Pulls from the length of the loan in years from the bond dictionary using its unique ID. 
def years(ID):
	ID = str(ID)
	List2 = bondDictionary[ID]
	result = List2[2]
	return int(result)

# Takes the bond rating as an argument and returns the position that a "1" should have in 
# the initial array, starting from "0".
def position(Rating): 
	if Rating == "A": 
		return 0
	elif Rating == "B":
		return 1
	elif Rating == "C": 
		return 2
	elif Rating == "D": 
		return 3
	else:
		return 4

# The initial array initally contains five "0" positions.  A '1' is placed in 
# the position in the array where the computation of this array's dot product with the transition matrix 
# produces a column vector containing that bond type's (A, B, C, D or E) transition array.  	
def initialArray(ID):
 	bondYears = years(ID)
 	A = np.array([0,0,0,0,0])
	A[position(bondRating(ID))] = 1 
	return A

# Annual rate of return of the loan
def couponRate(ID): 
	ID =  str(ID) 
	List = bondDictionary[ID]
	result = List[0]
	return result
	
# The annual payoff of the loan including retured principle of the loan.  
def annualPayoff(ID):
 	payoff = 100/years(ID) + float(couponRate(ID))
 	payoff = float(payoff/100)
 	return payoff
 
# An array containing the annual payoff amounts. Position D is assumed to be  
def payoffArray(ID): 
	A = np.zeros((5), dtype=float)
	for i in range(0,3): 
		A[i] = annualPayoff(ID)
	A[3] = recoveryRate(ID)
	return A

# If a loan defaults, the amount to be recovered.  
def recoveryRate(ID): 
	ID =  str(ID) 
	List = bondDictionary[ID]
	result = List[4]
	return float(result)

# The Internal Rate of Return for a given loan.  
def loanIRR(ID): 
	Time = years(ID)
	Z = np.zeros(Time + 1)
	Z[0] = -1
	A = initialArray(ID)
	C = payoffArray(ID) 
	for i in range(1, (Time + 1)):
		Z[i] = A.dot(matrixPower(i)).dot(C)
	return np.irr(Z) 
	
print loanIRR("100001")
	




	
	
	

	
	

	