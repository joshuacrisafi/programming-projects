#Welcome! This is my first personal programming project. It is all about the game Chopsticks and playing it.
#There are several existing variants of the game, but I chose the one I played in my childhood.
#This version includes free splitting (so long as it does not produce an equivalent state)
#and damage rollover (tagging a 4 with a 3 yields a 2, not a 0).
#The purpose of this program is to experiment with artificial intelligence in a simple context.
#The AI in this program learns very quickly if you play against it. As you will see,
#it carries 2 separate systems of machine learning: one for offense and one for defense.
#For this reason, there is also an option to have the AI play against another AI.
#This mode can be toggled by commenting out an indicated line below, and it
#also suppresses all print statements for maximum efficiency.
#Otherwise, feel free to explore the code and see how it works. It took a few days of solid
#work, and my comments will be dispersed throughout for clarification. Happy reading!
import random #for AI random move selection

class chop: #This program fundamentally runs on OOP. The entirety of the game is contained within a class and its methods/variables.
    def __init__(self):
        open('avoid.txt', 'a').close() #creates the file in question if it does not yet exist but does not modify it if it does
        open('take.txt', 'a').close() #creates the file in question if it does not yet exist but does not modify it if it does
        open('win.txt', 'a').close() #creates the file in question if it does not yet exist but does not modify it if it does
        file1 = open("avoid.txt","r") #This file is used for the defensive portion of the AI. It keeps track of which gamestates to avoid if at all possible.
        file2 = open("take.txt","r") #This file is used for the offensive portion of the AI. It keeps track of which gamestates to chase after if at all possible.
        file3 = open("win.txt","r") #This file is used for the offensive portion of the AI as well. It keeps track of which gamestates give the AI an option to create a gamestate in take.txt (the above list).
        self.player="AI" #This is the default in case the line below is commented out for AI training mode. Otherwise, it does not matter.
        self.player=input("Type AI to have the AI play for you. Otherwise, press ENTER.\n") #Comment out this line for AI training mode. It will suppress all print statements and have the AI play against a randomly-acting AI (with all legal moves of course)
        self.hands=[1,1,1,1] #This variable keeps track of the gamestate. The first 2 numbers are the player's hands, and the second 2 are the AI's hands.
        self.tCount=0 #Turn count
        self.moves=['tlwl','tlwr','trwl','trwr','s11','s02','s12','s03','s13','s22','s04','s14','s23','s24','s33','concede'] #All possible moves. They are explained further below.
        self.avoid=[] #Internal storage version of avoid.txt
        self.take=[]
        self.win=[]
        for line in file1.readlines(): #copies avoid.txt to self.avoid
            self.avoid.append(line.rstrip('\n'))
        file1.close()
        for line in file2.readlines():
            self.take.append(line.rstrip('\n'))
        file2.close()
        for line in file3.readlines():
            self.win.append(line.rstrip('\n'))
        file3.close()
        self.pLast=[1,1,1,1] #keeps track of positions so the AI can learn what it did right/wrong
        self.oLast=[1,1,1,1] #keeps track of positions so the AI can learn what it did right/wrong
        self.cur=list(range(len(self.moves)-1)) #This list is used to have the AI randomly select a move (the -1 is to prevent it from selecting "concede" at the end of self.moves)
        if(self.goFirst()):
            self.pTurn()
        else:
            self.oTurn()
    def goFirst(self):
        if(self.player==""): #If PLAYER is playing
            return input("Who will go first? (me/you only): \n")=="me"
        else: #If AI is playing, pick randomly who goes first
            return bool(random.getrandbits(1))
    def youWin(self): #What happens if player wins
        if(str(self.pLast) not in self.avoid):
            self.avoid.append(str(self.pLast))
            mod1=[self.pLast[1],self.pLast[0],self.pLast[2],self.pLast[3]]
            mod2=[self.pLast[0],self.pLast[1],self.pLast[3],self.pLast[2]]
            mod3=[self.pLast[1],self.pLast[0],self.pLast[3],self.pLast[2]]
            if(str(mod1) not in self.avoid):
                self.avoid.append(str(mod1))
            if(str(mod2) not in self.avoid):
                self.avoid.append(str(mod2))
            if(str(mod3) not in self.avoid):
                self.avoid.append(str(mod3))
        file1 = open("avoid.txt","w")
        for line in self.avoid: #Updates all 3 text files in the lines below
            file1.write(line+'\n')
        file1.close()
        file2 = open("take.txt","w")
        for line in self.take:
            file2.write(line+'\n')
        file2.close()
        file3 = open("win.txt","w")
        for line in self.win:
            file3.write(line+'\n')
        file3.close()
        plural="s"
        if(self.tCount==1):
            plural=""
        if(self.player==""):
            print(f"You won in {self.tCount} turn{plural}! The AI will be changed.")
        quit()
    def youLose(self,type="not concede"):
        if(str(self.hands) not in self.take):
            mod1=[self.hands[1],self.hands[0],self.hands[2],self.hands[3]]
            mod2=[self.hands[0],self.hands[1],self.hands[3],self.hands[2]]
            mod3=[self.hands[1],self.hands[0],self.hands[3],self.hands[2]]
            self.take.append(str(self.hands))
            if(str(mod1) not in self.take):
                self.take.append(str(mod1))
            if(str(mod2) not in self.take):
                self.take.append(str(mod2))
            if(str(mod3) not in self.take):
                self.take.append(str(mod3))
        if(str(self.oLast) not in self.win):
            mod1=[self.oLast[1],self.oLast[0],self.oLast[2],self.oLast[3]]
            mod2=[self.oLast[0],self.oLast[1],self.oLast[3],self.oLast[2]]
            mod3=[self.oLast[1],self.oLast[0],self.oLast[3],self.oLast[2]]
            self.win.append(str(self.oLast))
            if(str(mod1) not in self.win):
                self.win.append(str(mod1))
            if(str(mod2) not in self.win):
                self.win.append(str(mod2))
            if(str(mod3) not in self.win):
                self.win.append(str(mod3))
        if(type!="concede"): #If you concede, the AI didn't really win, so it does not change the text files.
            file1 = open("avoid.txt","w")
            for line in self.avoid:
                file1.write(line+'\n')
            file1.close()
            file2 = open("take.txt","w")
            for line in self.take:
                file2.write(line+'\n')
            file2.close()
            file3 = open("win.txt","w")
            for line in self.win:
                file3.write(line+'\n')
            file3.close()
        plural="s"
        if(self.tCount==1):
            plural=""
        if(self.player==""):
            if(type=="concede"):
                negative="will not"
            else:
                negative="may"
            print(f"You lost in {self.tCount} turn{plural}! The AI {negative} be changed.")
        quit()
    def validSplit(self,command,person="player",state=[]): #Determines whether or not a split is valid for the given player and in the given gamestate.
        if(state==[]):
            state=self.hands #The reason why this exists both here and in other functions below is that I cannot set self.hands as a function parameter default value below the "self" parameter is understood.
        if(person=="player"):
            offset=0 #checking if the PLAYER can do this split
        else:
            offset=2 #checking if the AI can do this split
        value1=state[offset]
        value2=state[offset+1]
        return ((value1==int(command[1]) and value2==int(command[2])) or (value1==int(command[2]) and value2==int(command[1])))==False and value1+value2==int(command[1])+int(command[2]) #checks that split is not equivalent to original state and does not change sum of hands
    def validTag(self,command,person="player",state=[]): #Determines whether or not a split is valid for the given player and in the given gamestate.
        if(state==[]):
            state=self.hands
        if(person=="player"):
            offset=0
        else:
            offset=2
        if(command[3]=='l'):
            From=offset
        else:
            From=offset+1
        if(command[1]=='l'):
            To=2-offset
        else:
            To=3-offset
        return state[From]!=0 and state[To]!=0 #just checks that the 2 relevant values in the tag are nonzero
    def bal(self): #balances the hands (ex. if they are more than 4) and checks for victory/defeat
        for hand in range(len(self.hands)):
            if(self.hands[hand]>4):
                self.hands[hand]-=5
        if(self.hands[2]==0 and self.hands[3]==0):
            self.youWin()
        elif(self.hands[0]==0 and self.hands[1]==0):
            self.youLose()
    def pTag(self,command): #Called to execute the given tag command on PLAYER's turn.
        if(command[3]=='l'):
            From=0
        else:
            From=1
        if(command[1]=='l'):
            To=2
        else:
            To=3
        self.hands[To]+=self.hands[From]
        self.bal()
        self.cur=list(range(len(self.moves)-1)) #for self.oTurn() below
        self.oLast=self.hands.copy()
        self.oTurn()
    def oTag(self,command): #Called to execute the given tag command on AI's turn.
        if(command[3]=='l'):
            From=2
        else:
            From=3
        if(command[1]=='l'):
            To=0
        else:
            To=1
        self.hands[To]+=self.hands[From]
        self.bal()
        self.pTurn()
    def pSplit(self,command): #Called to execute the given split command on PLAYER's turn.
        self.hands[0]=int(command[1])
        self.hands[1]=int(command[2])
        self.bal()
        self.cur=list(range(len(self.moves)-1))
        self.oLast=self.hands.copy()
        self.oTurn()
    def oSplit(self,command): #Called to execute the given split command on AI's turn.
        self.hands[2]=int(command[1])
        self.hands[3]=int(command[2])
        self.bal()
        self.pTurn()
    def oApply(self,command,state=[]): #Called to hypothetically determine the gamestate if the AI were to make the given move without actually making it (this function does not alter the actual gamestate)
        if(state==[]):
            state=self.hands
        copy=state.copy() #works on a copy of the state instead of modifying the original
        if(command[0]=='t'):
            if(command[3]=='l'):
                From=2
            else:
                From=3
            if(command[1]=='l'):
                To=0
            else:
                To=1
            copy[To]+=copy[From]
        else:
            copy[2]=int(command[1])
            copy[3]=int(command[2])
        for hand in range(len(copy)):
            if(copy[hand]>4):
                copy[hand]-=5
        return copy
    def pApply(self,command,state=[]): #Same as self.oApply, but for determining what the gamestate would be if PLAYER executed the given command.
        if(state==[]):
            state=self.hands
        copy=state.copy()
        if(command[0]=='t'):
            if(command[3]=='l'):
                From=0
            else:
                From=1
            if(command[1]=='l'):
                To=2
            else:
                To=3
            copy[To]+=copy[From]
        else:
            copy[0]=int(command[1])
            copy[1]=int(command[2])
        for hand in range(len(copy)):
            if(copy[hand]>4):
                copy[hand]-=5
        return copy
    def takeInput(self): #receives valid input from PLAYER on their turn
        if(self.player==""):
            print("Enter a command From the following list:",end=" ")
            for move in self.moves: #loop written to allow self.moves to be adjusted manually without having to rewrite this code. This would be useful if one wanted to change the rules of the game (just keep "concede" at the end of the list for other reasons).
                print(move,end="")
                if(move=='tlwl'):
                    print(' (tag left with left)',end=", ") #explains acronym
                elif(move=='s11'):
                    print(' (split into a 1 and a 1)',end=", ") #explains acronym
                elif(move!="concede"):
                    print(", ",end="")
                else:
                    print(".",end="") #concede is at the end.
            command=input("\n")
        else: #if it's AI vs AI, have the "player" choose a random move and check if it is valid.
            ran=random.choice(self.cur)
            command=self.moves[ran]
        if(command not in self.moves): #if invalid, try again
            if(self.player==""):
                print("Please try again. Be sure To enter something from the list below.")
            self.takeInput()
        else:
            if(command=="concede"):
                self.youLose("concede")
            elif(command[0]=="t"):
                if(self.validTag(command)):
                    self.pTag(command)
                else:
                    if(self.player==""):
                        print("Please try again. Be sure To enter a valid move.")
                    else:
                        self.cur.remove(ran)
                    self.takeInput()
            else:
                if(self.validSplit(command)):
                    self.pSplit(command)
                else:
                    if(self.player==""):
                        print("Please try again. Be sure To enter a valid move.")
                    else:
                        self.cur.remove(ran)
                    self.takeInput()
    def pTurn(self): #Start of your turn (before input received)
        self.tCount+=1
        if(self.tCount>20): #The turn count limit, imposed to keep all games of AI vs. AI within a set time constraint
            if(self.player==""):
                print("Maximum number of turns reached. Stalemate declared. Victory is awarded to the AI.")
            self.youLose("concede")
        self.cur=list(range(len(self.moves)-1)) #initialized for self.takeInput() below
        self.pLast=self.hands.copy() #saves a copy of the gamestate
        if(self.player==""): #PLAYER interface
            print(f"-----------------------------------------------------Turn {self.tCount}----------------------------------------------------")
            print(f"My Hands:             {self.hands[2]}     {self.hands[3]}")
            print(f"Your Hands:           {self.hands[0]}     {self.hands[1]}")
        self.takeInput()
    def validityCheck(self,command,player="opponent",state=[]): #one-size-fits-all validity-checking function
        if(state==[]):
            state=self.hands
        if(command[0]=='t'):
            return(self.validTag(command,player,state))
        else:
            return(self.validSplit(command,player,state))
    def oDo(self,command): #do the given command for the opponent
        if(command[0]=="t"):
            self.oTag(command)
        else:
            self.oSplit(command)
    def pOptions(self,state): #returns a list of possible player moves starting at the given state
        options=[]
        nonConcede=self.moves.copy()
        nonConcede.remove("concede")
        for move in nonConcede:
            if(self.validityCheck(move,"player",state)):
                options.append(self.pApply(move,state))
        return options
    def takeTest(self,state): #tests if a given state is known to have the AI surely win and adds it it self.take if so.
        check=True
        options=self.pOptions(state)
        for option in options:
            if(str(option) not in self.win):
                check=False
        if(check):
            if(str(state) not in self.take):
                mod1=[state[1],state[0],state[2],state[3]]
                mod2=[state[0],state[1],state[3],state[2]]
                mod3=[state[1],state[0],state[3],state[2]]
                self.take.append(str(state))
                if(str(mod1) not in self.take):
                    self.take.append(str(mod1))
                if(str(mod2) not in self.take):
                    self.take.append(str(mod2))
                if(str(mod3) not in self.take):
                    self.take.append(str(mod3))
        return check
    def oTurn(self,type="finish"): #opponent's turn (where most of the opponent AI stuff happens)
        if(len(self.cur)==0): #if the current "type" has no possible moves, roll over to the next one (finish->offense->defense->survival).
#Finish mode is where the AI tries to make a move that defeats the PLAYER instantly (not in several moves).
#Offense mode is where the AI tries to make a move that assures the AI's eventual victory.
#Defense mode is where the AI tries to make any move that is not in self.avoid (so any move that does not have a history of making the AI lose)
#Survival mode is where the AI gives up and uses any valid move.
            if(type=="offense"):
                self.cur=list(range(len(self.moves)-1)) #re-initializes self.cur before calling itself in the next type
                self.oTurn("defense")
            elif(type=="defense"): #If the AI finds itself unable to defend in a given position, that must mean that that position that its previous move was a mistake (or it had been trapped for several moves).
#So it adds the last recorded gamestate before the PLAYER moved (and all equivalent permutations) to self.avoid so that it does not make the same mistake again.
                if(str(self.pLast) not in self.avoid):
                    self.avoid.append(str(self.pLast))
                    mod1=[self.pLast[1],self.pLast[0],self.pLast[2],self.pLast[3]]
                    mod2=[self.pLast[0],self.pLast[1],self.pLast[3],self.pLast[2]]
                    mod3=[self.pLast[1],self.pLast[0],self.pLast[3],self.pLast[2]]
                    if(str(mod1) not in self.avoid):
                        self.avoid.append(str(mod1))
                    if(str(mod2) not in self.avoid):
                        self.avoid.append(str(mod2))
                    if(str(mod3) not in self.avoid):
                        self.avoid.append(str(mod3))
                self.cur=list(range(len(self.moves)-1))
                self.oTurn("survival")
            else: #In the case of type=="finish":
                self.cur=list(range(len(self.moves)-1))
                self.oTurn("offense")
        else:
            ran=random.choice(self.cur)
            command=self.moves[ran]
            if(not self.validityCheck(command)): #invalid move
                self.cur.remove(ran)
                self.oTurn(type)
            else:
                if(type=="defense"):
                    if(str(self.oApply(command)) in self.avoid):
                        self.cur.remove(ran)
                        self.oTurn("defense")
                    else:
                        self.oDo(command)
                elif(type=="offense"):
                    if(str(self.oApply(command)) in self.take): #if the given move would create a gamestate known to assure victory
                        if(str(self.hands) not in self.win): #adds the pre-move gamestate to self.win
                            mod1=[self.hands[1],self.hands[0],self.hands[2],self.hands[3]]
                            mod2=[self.hands[0],self.hands[1],self.hands[3],self.hands[2]]
                            mod3=[self.hands[1],self.hands[0],self.hands[3],self.hands[2]]
                            self.win.append(str(self.hands))
                            if(str(mod1) not in self.win):
                                self.win.append(str(mod1))
                            if(str(mod2) not in self.win):
                                self.win.append(str(mod2))
                            if(str(mod3) not in self.win):
                                self.win.append(str(mod3))
                        self.oDo(command)
                    elif(self.takeTest(self.oApply(command))): #just because the resulting gamestate isn't in self.take doesn't mean it shouldn't be. This line tests that and adds it if belongs there.
                        self.oDo(command)
                    else:
                        self.cur.remove(ran)
                        self.oTurn("offense")
                elif(type=="finish"):
                    result=self.oApply(command)
                    if(result[0]==0 and result[1]==0): #only agree to the move if it defeats PLAYER
                        self.oDo(command)
                    else:
                        self.cur.remove(ran)
                        self.oTurn("finish")
                else:
                    self.oDo(command)
chop=chop() #calls the entire program by initializing an instance of the class.
