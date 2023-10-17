Pc = 0 # Program counter (what part of the code is it on currently)
Ram = ['000'] * 100 #Ram Slots
Acc = 0 #accumulator
inbox = "" #input
outbox = "" #Output
halt = False #Stop yes or no?
Overflow = False #over 999 or under 0
debug = True #the debugger will run



program = [
  "901",
  "340",
  "901",
  "140",
  "902"
]

def dump(): #print out the computers state, such as the Ram, accumulator ect
  if not debug:
    return
  global Pc, Ram, Acc, Overflow, inbox, outbox
  print(f"Program Counter: {Pc}\n Ram: {Ram}\n Acc: {Acc}\n Outbox: {outbox}\n Inbox: {inbox}\n Overflow: {Overflow}")

def reset(): #reset the computer
  global halt, Pc, Ram, Acc, inbox, outbox, Overflow
  Pc = 0 # Program counter
  Ram = ['000'] * 100 #Ram Slots
  Acc = 0 #accumulator
  inbox = "" #input
  outbox = "" #Output
  halt = False #Stop yes or no?
  Overflow = False #over 999 or under 0
  debug("------------------------------------RESET FINISHED------------------------------------")

def load_program(program): #load the program
  reset()
  global Ram
  for x in range(0, len(program)):
    Ram[x] = program[x]
  
  debug(Ram)

def step(): #'ticks'. It will do the instruction then STEP to the next instruction.
  global halt, Ram, Pc

  while not halt: #while halt is false. 
    Op = Ram[Pc] #operation counter is whatever the Pc is looking at (Getting the instruction)
    debug(f"Step: OpCode = {Op}")

    #Instruction Decoding

    if Op == "000": # Halt
      hlt()
    
    elif Op == "901": # Input
      inp()

    elif Op == "902": # Output
      out()

    elif Op[0] == "1": # Add
      add(Op[1:]) #remove the 1 from the message

    elif Op[0] == "2": # Subtract
      sub(Op[1:]) #remove the 2 from the message

    elif Op[0] == "3": # Store
      sto(Op[1:]) # remove the 3 from the message
    
    elif Op[0] == "5": # Loads a ram slot
      lda(Op[1:]) #remove the 5 from the message

    elif Op[0] == "6": #Branch if the accumulator is zero
      bra(Op[1:]) #removes the 6 from the message

    else:
      raise Exception(f"OP code {Op} is not found. Halting...")

    Pc += 1 #increment the program counter

###----------functions----------------------------------------------------------------###

def inp(): #input data
  global Acc
  Acc = int(input("Enter Value: "))
  debug(f"Added {str(Acc)} to the accumulator")

def add(location): #add two num
  location = int(location)
  global Acc, Ram
  value = int(Ram[location])
  AccValue = int(Acc)
  AccValue += value

  if AccValue == (AccValue % 999) - 1:
    AccValue = (AccValue % 999)  - 1
  
  Acc = str(AccValue)
  AccLength = len(Acc)

  if AccLength == 1:
    Acc = "00" + Acc
  elif AccLength == 2:
    Acc = "0" + Acc
  elif AccLength == 3:
    raise Exception("Imputed data is to long")
  
  else:
    output = f"Added {value} to accumulator"
    debug(output)

def sub(location):
  location = int(location)
  global Acc, Ram
  AccValue = int(Acc)
  RamValue = int(Ram[location])
  AccValue -= RamValue

  if AccValue == (AccValue % 999) - 1:
      AccValue = (AccValue % 999)  - 1

  Acc = str(AccValue)
  AccLength = len(Acc)
  
  if AccLength == 1:
    Acc = "00" + Acc
  elif AccLength == 2:
    Acc = "0" + Acc
  elif AccLength == 3:
    raise Exception("Imputed data is to long")
  
  else:
    output = f"Subtracted {RamValue} from {AccValue}"
    debug(output)


def sto(location):  #store
  location = int(location)
  global Ram

  if Ram[location] == "000": # Checking if the ram slot is available
    Ram[location] = Acc
  else:
    debug("Ram slot is occupied. Cannot store.")
  debug(f"Stored {location}")

def out(): #output
  global Acc
  print(f"Output: {Acc}")

def hlt(): #halt, stop
  global halt
  halt = True
  print("Going for a coffee break")

def lda(location):
  location = int(location)
  global Acc, Ram
  Acc = int(Ram[location])

def bra(location):
  location = int(location)
  global Pc
  Pc = location

def brp(location):
  location = int(location)
  global Pc, Acc
  if Acc != '0':
    Pc = location
  else:
    debug("Smaller then 1")

def brz(location):
  location = int(location)
  global Pc, Acc
  if Acc == '0':
    Pc = location
  else:
    debug("Larger than 0")

def debug(message): # to debug the program
  global debug
  if debug:
    print(message)



debug("LMC is Starting...")

load_program(program)
step()
dump()
debug("Done")
