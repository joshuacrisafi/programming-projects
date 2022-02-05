#Welcome! This is a simple but powerful derivative calculator that runs on OOP and stores results in a data file automatically for efficiency and for the sake of logging all intermediate computations.
import itertools
from typing import Dict
from typing import List
import ast
import time

termList=['x','sin(x)','cos(x)','sinh(x)','cosh(x)','e^x','ln(x)'] #To add a new function to the program's list of functions, just enter its string representation here and add its derivative in array notation on line 10.
termNum=len(termList)
primitiveDerivatives=[[[[0,0,0,0,0,0,0],1.0]],[[[0,0,1,0,0,0,0],1.0]],[[[0,1,0,0,0,0,0],-1.0]],[[[0,0,0,0,1,0,0],1.0]],[[[0,0,0,1,0,0,0],1.0]],[[[0,0,0,0,0,1,0],1.0]],[[[-1,0,0,0,0,0,0],1.0]]] #respective array representations of the derivatives of the primitive functions on line 8.
maxDepth=1000-3-termNum

def differentiateTerm(inputTerm,differentiate): #uses the 'differentiate' dictionary and the product/quotient rule to find the derivative of a lone term
    term=Term(inputTerm.factors.copy(),inputTerm.coeff)
    if term in differentiate:
        return differentiate[term]
    else:
        i=0
        while(i<len(term.factors) and term.factors[i]==0):
            i+=1
        if(i==len(term.factors)):
            raise Exception("Error: derivatives.txt contains incomplete data for this calculation.")
        else:
            if(term.factors[i]<0):
                termA=Term(term.factors.copy(),1)
                termB=Term([0],1)
                termA.factors[i]=termA.factors[i]+1
                termB.factors[i]=1
                differentiate[term]=termB.timesFunc(differentiateTerm(termA,differentiate)).plusFunc(termA.timesFunc(differentiateTerm(termB,differentiate)).timesBy(-1)).divideFunc(termB.timesFunc(Function([termB])))
                return differentiate[term]
            else:
                termA=Term(term.factors.copy(),1)
                termB=Term([0],1)
                termA.factors[i]=termA.factors[i]-1
                termB.factors[i]=1
                differentiate[term]=termA.timesFunc(differentiateTerm(termB,differentiate)).plusFunc(termB.timesFunc(differentiateTerm(termA,differentiate)))
                return differentiate[term]

def findDerivative(f,differentiate): #finds the derivative of a function f by splitting it up into terms and calling differentiateTerm
    derivativeList=[]
    for term in f.tList:
        normal=Term(term.factors,1.0)
        c=term.coeff
        derivative=differentiateTerm(normal,differentiate)
        for result in derivative.tList:
            result=result.timesBy(c)
            derivativeList.append(result)
    return Function(derivativeList)

def coeffIntCheck(inputFloat): #small helper function to have floats like -7.0 display as -7 instead when printed
    if(inputFloat==int(inputFloat)):
        return int(inputFloat)
    else:
        return inputFloat

class Term: #a term is a product of factor functions (each with its own exponent) multiplied by some float coefficient
    coeff:float=1.0
    factors:List[int]=[]
    def __init__(self,inputList:List[int],inputC:float=1.0):
        if(len(inputList)>termNum):
            raise Exception(f"indexError: too many terms passed into inputList. max: {termNum}. passed: {len(inputList)}. values: {inputList}.")
        else:
            self.factors=inputList
            while(len(self.factors)<termNum):
                (self.factors).append(0)
            self.coeff=inputC
            if(self.coeff==0):
                for i in range(len(self.factors)):
                    self.factors[i]=0
    def __hash__(self): #must be hashable to be used in a dictionary
        return hash((self.coeff,tuple(self.factors)))
    def __eq__(self,other): #for dictionary support
        return (self.coeff,self.factors)==(other.coeff,other.factors)
    def toString(self): #very intricate toString method for user readability of functions
        sofar=""
        numerator=""
        denominator=""
        check=True
        for i in self.factors:
            if(i!=0):
                check=False
        if(check or self.coeff==0):
            return str(coeffIntCheck(self.coeff))
        else:
            if(self.coeff*self.coeff!=1):
                sofar+=str(coeffIntCheck(self.coeff))
            elif(self.coeff==-1):
                sofar+="-"
            for i in range(termNum):
                expo=self.factors[i]
                if(expo>0):
                    if(expo==1):
                        if(numerator==""):
                            numerator+=termList[i]
                        else:
                            numerator+="*"+termList[i]
                    else:
                        if(numerator==""):
                            numerator+=termList[i]+"^"+str(expo)
                        else:
                            numerator+="*"+termList[i]+"^"+str(expo)
                elif(expo<0):
                    if(expo==-1):
                        if(denominator==""):
                            denominator+=termList[i]
                        else:
                            denominator+="*"+termList[i]
                    else:
                        if(denominator==""):
                            denominator+=termList[i]+"^"+str(-expo)
                        else:
                            denominator+="*"+termList[i]+"^"+str(-expo)
            if(numerator=="" or numerator=="-"):
                numerator+="1"
            if(denominator==""):
                sofar+=numerator
            else:
                sofar+=numerator+"/("+denominator+")"
            return sofar
    def timesBy(self,constant):
        return Term(self.factors.copy(),self.coeff*constant)
    def timesTerm(self,other):
        prodList=[]
        for i in range(termNum):
            prodList.append(self.factors[i]+other.factors[i])
        return Term(prodList,self.coeff*other.coeff)
    def timesFunc(self,function):
        prodList=[]
        for funcTerm in function.tList:
            prodList.append(self.timesTerm(funcTerm))
        return Function(prodList)

class Function: #a function is defined as a sum of terms
    tList:List[Term]=[]
    def prune(self): #deletes terms of value zero (coefficient zero)
        offset=0
        nList=self.tList.copy()
        for i in range(len(nList)):
            if(nList[i].coeff==0):
                self.tList.pop(i-offset)
                offset+=1
    def groupTerms(self): #groups like terms. ex: 2x+3x=5x
        for i in range(len(self.tList)):
            for j in range(i+1,len(self.tList)):
                if(self.tList[i].factors==self.tList[j].factors):
                    self.tList[i]=Term(self.tList[i].factors,self.tList[i].coeff+self.tList[j].coeff)
                    self.tList[j]=Term([0],0.0)
    def __init__(self,inputList:List[Term]):
        self.tList=inputList
        self.groupTerms()
        self.prune()
    def __hash__(self): #for dictionary support
        return hash(tuple(self.tList))
    def __eq__(self,other): #for dictionary support
        return self.tList==other.tList
    def toString(self): #relies on the Term implementation of toString to do most of the work
        sofar=""
        for term in self.tList:
            if(sofar=="" or term.coeff<0):
                sign=""
            else:
                sign="+"
            sofar+=sign+term.toString()
        if(sofar==""):
            sofar="0"
        return sofar
    def plusFunc(self,other):
        sumList=[]
        for i in self.tList:
            sumList.append(i)
        for i in other.tList:
            sumList.append(i)
        return Function(sumList)
    def divideBy(self,constant):
        if(constant==0):
            raise Exception("Constant of value 0 passed into divideBy in Function class.")
        newFunc=Function(self.tList.copy())
        for term in newFunc.tList:
            term.coeff=term.coeff/constant
        return newFunc
    def timesBy(self,constant):
        newFunc=Function(self.tList.copy())
        for term in newFunc.tList:
            term.coeff=term.coeff*constant
        return newFunc
    def reciprocal(self):
        nList=[]
        for i in range(len(self.tList)):
            recipList=[]
            for j in range(len(self.tList[i].factors)):
                recipList.append(self.tList[i].factors[j]*-1)
            nList.append(Term(recipList,self.tList[i].coeff))
        newFunc=Function(nList)
        return newFunc
    def timesFunc(self,other):
        newFunc=Function([])
        for term in other.tList:
            newFunc=newFunc.plusFunc(term.timesFunc(self))
        return newFunc
    def divideFunc(self,other):
        return self.timesFunc(other.reciprocal())

def toList(string): #for turning a string representation of an array into an actual array
    return ast.literal_eval(string)

def toTerm(l): #list into term
    LIST=l.copy()
    tList=LIST[0]
    coeff=LIST[1]
    return Term(tList,coeff)

def toFunc(l): #list into function
    LIST=l.copy()
    for i in range(len(LIST)):
        LIST[i]=toTerm(LIST[i])
    return Function(LIST)

def checkDefaultDerivatives(differentiate): #makes sure that the derivatives of the primitive functions are both in 'differentiate' and are correct
    LIST=[]
    for j in range(termNum):
        LIST.append(0)
    term=toTerm([LIST.copy(),0.0])
    if term not in differentiate:
        differentiate[term]=Function([term])
    elif differentiate[term]!=Function([term]):
        print(f"Invalid derivative detected in derivatives.txt. Correcting now.")
        differentiate[term]=Function([term])
    newTerm=toTerm([LIST.copy(),1.0])
    if newTerm not in differentiate:
        differentiate[newTerm]=Function([term])
    elif differentiate[newTerm]!=Function([term]):
        print(f"Invalid derivative detected in derivatives.txt. Correcting now.")
        differentiate[newTerm]=Function([term])
    for i in range(termNum):
        LIST=[]
        for j in range(termNum):
            if(j==i):
                LIST.append(1)
            else:
                LIST.append(0)
        term=toTerm([LIST.copy(),1.0])
        if term not in differentiate:
            differentiate[term]=toFunc(primitiveDerivatives[i])
        elif differentiate[term]!=toFunc(primitiveDerivatives[i]):
            print(f"Invalid derivative detected in derivatives.txt. Correcting now.")
            differentiate[term]=toFunc(primitiveDerivatives[i])

def readDerivatives(): #read derivatives from derivatives.txt and records them in 'differentiate', which is a dictionary
    differentiate={}
    open("derivatives.txt","a").close()
    with open('derivatives.txt','r') as file1:
        for line in file1.readlines():
            pair=toList(line.rstrip('\n'))
            func1=toTerm(pair[0])
            func2=toFunc(pair[1])
            differentiate[func1]=func2
    checkDefaultDerivatives(differentiate)
    return differentiate

def termToArrayString(term): #converts a term to a string in array representation and removes the spaces
    return str([term.factors,term.coeff]).replace(" ","")

def funcToArrayString(function): #converts a function to a string in array representation
    if(len(function.tList)==0):
        return "[]"
    sofar="["
    for term in function.tList:
        sofar+=termToArrayString(term)+","
    return sofar[:-1]+"]"

def writeDerivatives(differentiate): #writes data from 'differentiate' to derivatives.txt
    with open('derivatives.txt','w') as file1:
        for function in differentiate:
            file1.write(f"[{termToArrayString(function)},{funcToArrayString(differentiate[function])}]\n")

def listAbsSum(LIST): #helper function for below (to avoid hitting recursion depth limit)
    total=0
    for i in LIST:
        if(i>=0):
            total+=i
        else:
            total-=i
    return total

def readTerm(): #reads a term from the user
    factors=[]
    check=True
    while(check):
        try:
            coefficient=float(input("First, enter the coefficient of your term (a real number in decimal notation):\n"))
            if(coefficient)==0:
                if(input("Warning: a coefficient of 0 will make the entire term null and void. Is this okay? (yes/no):\n")=="yes"):
                    return Term([0],0.0)
                else:
                    print("Coefficient input discarded.")
            else:
                check=False
        except:
            print("Error: invalid input discarded.")
    for i in range(termNum):
        check=True
        while(check):
            try:
                temp=int(input(f"Next, enter the exponent of {termList[i]} in your term (integers only):\n"))
                if(temp>=0):
                    if(listAbsSum(factors)+temp<=maxDepth):
                        validInput=True
                    else:
                        validInput=False
                else:
                    if(listAbsSum(factors)-temp<=maxDepth):
                        validInput=True
                    else:
                        validInput=False
                if(validInput):
                    factors.append(temp)
                    check=False
                else:
                    print(f"Error: exponent out of bounds. The sum of the absolute values of your exponents must not exceed {maxDepth}.")
            except:
                print("Error: invalid input discarded.")
    return Term(factors,coefficient)

def readInput(): #reads a function from the user
    funcList=[readTerm()]
    while(input("Add another term to your function? (yes/no):\n")=="yes"):
        funcList.append(readTerm())
    return Function(funcList)

def main():
    print("Welcome to the derivative calculator! You will now be instructed in entering your input function (what you want to differentiate).")
    differentiate=readDerivatives()
    inputFunc=readInput()
    startTime=time.time() #used to time the process
    outputFunc=findDerivative(inputFunc,differentiate)
    endTime=time.time() #used to time the process
    print(f"The derivative of {inputFunc.toString()} is {outputFunc.toString()}. It took me {endTime-startTime} seconds to make that computation.")
    writeDerivatives(differentiate)

if(__name__=="__main__"):
    main()
