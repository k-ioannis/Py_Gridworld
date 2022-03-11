import math
import random
import time 
import numpy
from dataclasses import dataclass

@dataclass 
class Enviroment:
    b_Rows    : int 
    b_Columns : int 
    Board     : list
    Terminal  : list 

@dataclass 
class Agent: 
    tr_Board      : list 
    cur_Index     : int 
    learning_Rate : float
    

def set_Enviroment():
    
    b_Rows      = 4
    b_Columns   = 4  
    print("Grid dimiensions :", b_Rows,"*", b_Columns)
    Row     = []
    Board   = []

    for i in range(b_Rows):
        for j in range(b_Columns):
            
            #Initializing the rows
            Row.append( "n" )
        
        #Filling the board with rows 
        Board.append(Row)
        Row     = []
    
    #Getting the two terminal states
    Terminal = []
    
    #Terminal.Point.Index 1
    TPI1 = 0

    
    #Terminal.Point.Index 2
    TPI2 = 15

    #Converitng them to array indexes
    row   =  int (TPI1 / b_Rows)
    col   =  int (TPI1 % b_Columns)
    Board [ row ] [ col ] = "t"
    
    row   =  int (TPI2 / b_Rows)
    col   =  int (TPI2 % b_Columns)
    Board [ row ] [ col ] = "t"
    
    Terminal.append(TPI1)
    Terminal.append(TPI2)
    print("Enviroment: ")
    for i in range(b_Rows): 
        print(Board[i])
    
    return b_Rows, b_Columns, Board, Terminal 


def set_Agent( Env ):
    
    tr_Board = []
    Row      = []
    
    #Initializing the agent array 
    print("Agent Array:")
    for i in range( Env.b_Rows ):
        for j in range( Env.b_Columns ):
                Row.append(0)
                
        tr_Board.append( Row )
        Row = []

    for i in range( Env.b_Rows * Env.b_Columns ):
        
        if i in Env.Terminal:
            row = int( i / Env.b_Rows )
            col = i % Env.b_Columns
            tr_Board[row][col] = 1
            
    for i in range( Env.b_Rows ):
        print (tr_Board[i])
    
    return tr_Board


def validate_Moves( Env, Agent ):
    
    index = Agent.cur_Index
    
    if(index == 0):
        
        return index + 0, index + 1, index + 4, index + 0 
    
    if(index == 1):
        
        return index - 1, index + 1, index + 4, index + 0
    
    if(index == 2):
        
        return index - 1, index + 1, index + 4, index + 0 
    
    if(index == 3):

        return index - 1, index + 0, index + 4, index + 0    
    
    if(index == 4):
    
        return index + 0, index + 1, index + 4, index - 4
    
    if(index == 5):
        
        return index - 1, index + 1, index + 4, index - 4
    
    if(index == 6):
    
        return index - 1, index + 1, index + 4, index - 4
    
    if(index == 7):
    
        return index - 1, index + 0, index + 4, index - 4
    
    if(index == 8):
    
        return index - 0, index + 1, index + 4, index - 4
    
    if(index == 9):
    
        return index - 1, index + 1, index + 4, index - 4
     
    if(index == 10):
    
        return index - 1, index + 1, index + 4, index - 4
    
    if(index == 11):
    
        return index - 1, index + 0, index + 4, index - 4
    
    if(index == 12):
    
        return index - 0, index + 1, index + 0, index - 4
    
    if(index == 13):
    
        return index - 1, index + 1, index + 0, index - 4
    
    if(index == 14):
    
        return index - 1, index + 1, index + 0, index - 4
    
    if(index == 15):
    
        return index - 1, index + 0, index + 0, index - 4

def Expected_Value( Env, Agent,  left, right, down, up ):
    
    v_List=[-1,-1,-1,-1]
    max_Reward=[]
    v = 0

    #print("    Possible moves:", left , right, down, up )
    
    #Checking expected value of moving left
    #if it doesnt bouce back 
    if left != Agent.cur_Index:
        
        row = int(left / Env.b_Rows)
        col = left % Env.b_Columns
        v_List[0] = Agent.tr_Board[row][col]
        
    #Cheking expected value of moving right
    #if it doesnt bouce back 
    if right != Agent.cur_Index:
        
        row = int(right / Env.b_Rows)
        col = right % Env.b_Columns
        v_List[1] = Agent.tr_Board[row][col]

        
    #Checking expected value of moving down
    #if it doesnt bouce back 
    if down != Agent.cur_Index:
        
        row = int(down / Env.b_Rows)
        col = down % Env.b_Columns
        v_List[2] = Agent.tr_Board[row][col]
        
    #Checking expected value of moving up
    #if it doesnt bouce back 
    if up != Agent.cur_Index:
            
        row = int(up / Env.b_Rows)
        col = up % Env.b_Columns
        v_List[3] = Agent.tr_Board[row][col]
        
    #print(v_List)
    

    max_Reward.append( numpy.argmax(v_List) )
    for i in range( len(v_List) ):
        if i != max_Reward[0] and v_List[i] == v_List[max_Reward[0]]:
            max_Reward.append( i )
    
    #print(max_Reward)
    
    row = int( Agent.cur_Index / Env.b_Rows )
    col = int( Agent.cur_Index % Env.b_Columns )
    
    Env.Board[row][col] = ""
    
    if 0 in max_Reward:
        #print("    Max reward:", v_List[0] ,"Moving: ←")
        Env.Board[row][col] += "←"    
        
        v_st  = Agent.tr_Board [row][col]
        v_st1 = Agent.tr_Board [row][col - 1]
        
        v = v_st + Agent.learning_Rate * ( v_st1 - v_st )
        
    if 1 in max_Reward:
        #print("    Max reward:", v_List[1] ,"moving: →")
        Env.Board[row][col] += "→" 
        
        v_st  = Agent.tr_Board [row][col]
        v_st1 = Agent.tr_Board [row][col + 1]
        
        v = v_st + Agent.learning_Rate * ( v_st1 - v_st )
        
    if 2 in max_Reward:
        #print("    Max reward:", v_List[2] ,"moving: ↓")
        Env.Board[row][col] += "↓" 
        
        v_st  = Agent.tr_Board [row][col]
        v_st1 = Agent.tr_Board [row + 1][col]
        
        v = v_st + Agent.learning_Rate * ( v_st1 - v_st )
        
        
    if 3 in max_Reward:
        #print("    Max reward:", v_List[3] ,"moving: ↑")
        Env.Board[row][col] += "↑" 
        
        v_st  = Agent.tr_Board [row][col]
        v_st1 = Agent.tr_Board [row - 1][col]
        
        v = v_st + Agent.learning_Rate * ( v_st1 - v_st )
    
    return v

def update_Policy( Env, Agent ):


    temp = []

    for index in range( Env.b_Columns * Env.b_Rows ):
        
        row = int( index / Env.b_Rows )
        col = index % Env.b_Rows
        
        if( Env.Board[row][col] != "t"):
            
            Agent.cur_Index = index
            left, right, down, up    =  validate_Moves( Env, Agent)
            #print(" Block: ", index)
            
            temp.append( Expected_Value( Env, Agent,  left, right, down, up ) )
        
        else:
            temp.append( Agent.tr_Board[row][col] )
    
    
        

    for i in range( Env.b_Columns * Env.b_Rows ):
        
        row = int( i / Env.b_Rows )
        col = i % Env.b_Rows
        
        Agent.tr_Board[row][col] = round(temp[i], 2)
        
    
    return 0 









b_Rows, b_Columns, Board, Terminal = set_Enviroment()
Env = Enviroment( b_Rows, b_Columns, Board, Terminal )
#Validation 
#print( b_Rows, b_Columns, Board )


tr_Board  = set_Agent( Env )
Agent     = Agent( tr_Board,0 ,0.5)
for  i in range(6):
    update_Policy(Env, Agent)
    
    time.sleep(2)
    print("EXPEVTED VALUES AFTER :", i + 1,"ITERATIONS")
    for k in (Agent.tr_Board):
        print(k)
    
    time.sleep(2)
    print("OPTIMAL TRANSITIONS:", i + 1,"ITERATIONS")
    for k in (Env.Board):
        print(k)

