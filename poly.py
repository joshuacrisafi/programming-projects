#Welcome! This is was a very short project. The goal of this code is mainly to find the generating series of a constant-recursive sequence. I had a class this past semester (Fall 2021) in which that exact computation was very very useful to know, so I decided to write a script to do it automatically. The other computations the program can perform are just there because I needed to code them anyway for the main computation.
#This project fundamentally runs on OOP by making both polynomials and series their own classes. Essentially, a polynomial is a coefficient list plus a degree, and a series is 2 polynomials. Further details are given in the comments below.
class series:
    num=0
    denom=0
    def toString(self):
        return "("+self.num.toString()+")/("+self.denom.toString()+")"
    def setDenom(self,recurrence): #sets the denominator given a recurrence passed into the constructor below
        for i in range(len(recurrence)-1,-1,-1): #this allows the denominator to be the negated and reversed order version of the recurrence. There is also a 0 at the start of it before the appending.
            self.denom.cList.append(-recurrence[i]) #the appending is direct here so as not to cause troubles with 0 being the leading coefficient.
            self.denom.degree+=1
        self.denom.cList[0]=1 #sets the constant term to 1, which it always is, instead of 0 as it was initialized.
        self.denom.prune()
    def setNum(self,init): #sets the numerator given a list of initial conditions passed into the constructor below
        values=polynomial([]) #values is equivalent to a truncated power series of the function. It is equivalent to performing polynomial long division on the numerator and denominator, but we are using this to compute the numerator, so this is like working backwards in a sense.
        values.cList=init
        values.degree=len(init)-1
        for i in range(len(init)+5):
            a=0
            for j in range(self.denom.degree):
                a+=-1*values.get(-j-1)*self.denom.get(j+1) #applying the initial conditions (stored in values) and the recurrence (stored in the denominator, which was computed directly from the recurrence)
            values.simpleAppend(a) #we don't want to have to worry about troubles with 0, so simpleAppend is used here
        values.degree=len(values.cList)-1
        first=values.times(self.denom).cList #gives our first guess for the numerator by multiplying the denominator by the truncated power series of the function
        a=0 #we will now add another term to values and then perform the multiplication again
        for j in range(self.denom.degree):
            a+=-1*values.get(-j-1)*self.denom.get(j+1)
        values.simpleAppend(a)
        values.degree=len(values.cList)-1
        second=values.times(self.denom).cList #this is now a second guess as to the true numerator
        a=0 #same process as above
        for j in range(self.denom.degree):
            a+=-1*values.get(-j-1)*self.denom.get(j+1)
        values.simpleAppend(a)
        values.degree=len(values.cList)-1
        third=values.times(self.denom).cList #this is now a third guess as to the true numerator
        nu=[] #final coefficients for numerator
        for i in range(len(self.denom.cList)-1): #the numerator must be of lesser degree than the denominator, so only these terms need be checked
            if(first[i]==second[i] and second[i]==third[i]): #if all 3 polynomials agree, it must be valid, and there is no way for them to agree without it being valid
                nu.append(first[i])
            else:
                nu.append(0) #this is why nu is not yet a polynomial: we must be able to append 0
        self.num=polynomial(nu)
    def __init__(self,recurrence,init): #calls the above functions
        self.num=polynomial([])
        self.denom=polynomial([])
        self.setDenom(recurrence)
        self.setNum(init)
class polynomial:
    cList=[] #coefficient list
    degree=0
    def monoMult(self,c,n): #multiplies by a monomial of the form c*x^n
        prod=[]
        for i in range(n):
            prod.insert(0,0)
        for i in range(self.degree+1):
            prod.append(c*self.get(i))
        product=polynomial(prod)
        return product
    def prune(self): #the most important function in the code. fixes empty coefficient lists and removes trailing zeroes (and fixes degree)
        if(self.cList==[]):
            self.cList=[0]
        while(self.cList[-1]==0 and len(self.cList)>1):
            self.cList.pop()
            self.degree-=1
        if(self.cList==[0]):
            self.degree=0
    def __init__(self,coefficients):
        self.cList=coefficients
        self.degree=len(coefficients)-1
        self.prune()
    def simpleAppend(self,value): #for appending when ending in a 0 is not a problem (does not prune)
        self.cList.append(value)
        self.degree+=1
    def get(self,i):
        return self.cList[i]
    def toString(self): #converts the polynomial into a string. takes great precaution for standardization of form
        sofar=""
        for i in range(self.degree,-1,-1):
            if(self.get(i)!=0):
                if(i==0):
                    power=""
                elif(i==1):
                    power="x"
                else:
                    power="x^"+str(i)
                if(self.get(i)<0):
                    sign="-"
                elif(sofar==""):
                    sign=""
                else:
                    sign="+"
                if((self.get(i)==1 or self.get(i)==-1) and i>0):
                    num=""
                elif(self.get(i)>0):
                    num=str(self.get(i))
                else:
                    num=str(-1*self.get(i))
                sofar+=sign+num+power
        if(sofar==""):
            sofar="0"
        return sofar
    def plus(self,other): #adds 2 polynomials and returns the sum. does not modify the state of either passed polynomial.
        maximum=max(self.degree,other.degree)
        sum=[]
        for i in range(maximum+1):
            sum.append(0)
        for i in range(maximum+1):
            if(i<=self.degree):
                sum[i]+=self.get(i)
            if(i<=other.degree):
                sum[i]+=other.get(i)
        sumPoly=polynomial(sum)
        return sumPoly
    def times(self,other): #multiplies 2 polynomials and returns the sum. does not modify the state of either passed polynomial.
        prod=polynomial([])
        for i in range(self.degree+other.degree+2):
            (prod.cList).append(0)
        prod.degree=self.degree+other.degree
        for i in range(other.degree+1):
            prod=prod.plus(self.monoMult(other.get(i),i)) #computation is done term-by-term with monomial multiplication.
        return prod
def gen(): #path to find generating series of a constant-recursive function
    check=True
    i=0
    re=[]
    while(check):
        if(i==0):
            try:
                re.append(int(input("Enter the coefficient of s(n) in the recurrence: ")))
                i+=1
            except:
                print("Please enter a valid integer or press ENTER.")
        else:
            a=input("Enter the coefficient of s(n+"+str(i)+") in the recurrence, or press ENTER to have everything so far be set equal to s(n+"+str(i)+"): ")
            try:
                if(a==""):
                    check=False
                else:
                    re.append(int(a))
                    i+=1
            except:
                print("Please enter a valid integer or press ENTER.")
    inn=[]
    for j in range(i):
        a=input("Enter the value of s("+str(j)+") (press ENTER to indicate 0): ")
        if(a==""):
            a="0"
        try:
            inn.append(int(a))
        except:
            print("Your input has been interpreted as 0, since it was not an integer.")
            inn.append(0)
    gen=series(re,inn)
    print("The generating series of this constant-recursive sequence is as follows: "+gen.toString())
    q()
def add(): #path to add 2 polynomials
    p1=[]
    p2=[]
    i=0
    while(i>=0):
        a=input("Enter the coefficient of x^"+str(i)+" in your first polynomial (press ENTER to finish): ")
        try:
            if(a==""):
                i=-1
            else:
                p1.append(int(a))
                i+=1
        except:
            print("Please enter a valid integer or press ENTER.")
    i=0
    while(i>=0):
        a=input("Enter the coefficient of x^"+str(i)+" in your second polynomial (press ENTER to finish): ")
        try:
            if(a==""):
                i=-1
            else:
                p2.append(int(a))
                i+=1
        except:
            print("Please enter a valid integer or press ENTER.")
    poly1=polynomial(p1)
    poly2=polynomial(p2)
    print("("+poly1.toString()+")+("+poly2.toString()+")="+poly1.plus(poly2).toString())
    q()
def mult(): #path to multiply 2 polynomials
    p1=[]
    p2=[]
    i=0
    while(i>=0):
        a=input("Enter the coefficient of x^"+str(i)+" in your first polynomial (press ENTER to finish): ")
        try:
            if(a==""):
                i=-1
            else:
                p1.append(int(a))
                i+=1
        except:
            print("Please enter a valid integer or press ENTER.")
    i=0
    while(i>=0):
        a=input("Enter the coefficient of x^"+str(i)+" in your second polynomial (press ENTER to finish): ")
        try:
            if(a==""):
                i=-1
            else:
                p2.append(int(a))
                i+=1
        except:
            print("Please enter a valid integer or press ENTER")
    poly1=polynomial(p1)
    poly2=polynomial(p2)
    print("("+poly1.toString()+")*("+poly2.toString()+")="+poly1.times(poly2).toString())
    q()
def main():
    a=input("Please select a computation to perform from the following list by entering its corresponding key:\n1: Add 2 polynomials\n2: Multiply 2 polynomials\n3: Find the generating series of a constant-recursive sequence\n4: Quit program\n")
    if(a=="1"):
        add()
    elif(a=="2"):
        mult()
    elif(a=="3"):
        gen()
def q():
    a=input("Make another computation? (y/n): ")
    if(a=="y" or a=="yes" or a=="Y" or a=="Yes" or a=="y." or a=="yes." or a=="Y." or a=="Yes."):
        main()
if(__name__=="__main__"):
    main()
