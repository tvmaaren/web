"""
Copyright <YEAR> <COPYRIGHT HOLDER>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""




import pdb

#in this version it is possible too ask a variable of the instruction before it is
#defined

assembly = input("wich file would you like to compile:");
cfile = open(assembly,'r+')

#make a new file
binary = input("wich file would you like to store the output too:")
out = open(binary,"w+")

#make the logisim file
logisim = open(binary + " logisim", "w+")


instructc=0
linec=1#wich instruction its busy with
emptyc = 0#counts how many lines in a row are empty. If this number
          #becomes greater than 20 it is assumed that the file has ended

string = cfile.readlines()

amlines =0
program = []#where all the binary is stored in text
var     = [[],[],[]]#where all variable information is stored
pvar    = [[],[],[]]#where the names, the addresses and the location in the file of the program labels are stored
reallinec = 0
section = "pgm" #in wich section of the program we, by default we are in the pgm section

#find the labels
i=0#counter
while(len(string)>reallinec):
    #continue adding words of the row too the list untill it 
    #finds an instruction, if it doesn't find an instruction it
    #should give an error message
    i=0#counter
    if(section == "pgm"):
        found = False#sais that there hasn't been a variable found in this specific line
        code = False#by default there is no code in the line
        while(1):#this will break when an instruction is found
            #retrieve the lable name
            label = ""
            length = len(string[reallinec])
            while(i<length):
                dbreak = False#sais if the loop should break
                #first it has to find the beginning of the word
                while(not(string[reallinec][i] == " " or string[reallinec][i] == "\t" or string[reallinec][i] == "\n")):
                    dbreak = True#the loop that goes throught the entire line should stop
                    if(string[reallinec][i] == "/"):
                        break
                    label = label+string[reallinec][i]
                    i = i+1
                if(dbreak):
                    break
                i = i+1
            #check if it is a valid label
            #check if it is an instruction
            if(label == "load" or label == "store" or label == "not" or label == "neg" or label == "add" or label == "and" or label == "jmp" or label == "skip"):
                #it can go too the next instruction
                linec = linec+1
                break
            #check if their is just nothing
            elif(label == ""):#there is nothing left in this line so it is finished here
                break
            #check if there is a new mode
            elif(label == "pgm"):
                break
            elif(label == "var"):
                section = "var"
                break
            else:#it is a label
                #first check if the label doesn't already exist
                e = False #the program shouldn't stop
                try:
                    print("the label " + label + " on line " + str(reallinec+1) + " already exists on line " + str(pvar[2][pvar[0].index(label)]+1))
                    e = True#the program should stop
                except:
                    pvar[0].append(label)
                    pvar[1].append(linec-1)
                    pvar[2].append(reallinec)
                if(e):
                    exit()
    else:#check if this string has pgm wich will change the mode
        label = ""
        length = len(string[reallinec])
        while(i<length):
            dbreak = False#sais if the loop should break
            #first it has to find the beginning of the word
            while(not(string[reallinec][i] == " " or string[reallinec][i] == "\t" or string[reallinec][i] == "\n")):
                dbreak = True#the loop that goes throught the entire line should stop
                if(string[reallinec][i] == "/"):
                    break
                label = label+string[reallinec][i]
                i = i+1
            if(dbreak):
                break
            i = i+1
        if(label == "pgm"):
            section = "pgm"       
    reallinec = reallinec +1

reallinec = 0
section = "pgm" #in wich section of the program we, by default we are in the pgm section
linec=1#wich instruction its busy with


while(reallinec<len(string)):
    length = len(string[reallinec])
    i=0#letter counter wich counts trough the string
    if(section == "var" or section == "const"):
        #retrieve the variable name
        variable = ""
        while(i<length):
            dbreak = False#sais if the loop should break
            #first it has to find the beginning of the word
            while(not(string[reallinec][i] == " " or string[reallinec][i] == "\t" or string[reallinec][i] == "\n")):
                dbreak = True#the loop that goes throught the entire line should stop
                if(string[reallinec][i] == "/"):
                    break
                variable = variable+string[reallinec][i]
                i = i+1
            if(dbreak):
                break
            i = i+1

        if(variable == ""):
            emptyc = emptyc+1
            if(emptyc > 20):
                print(program)
                print(var)
                amlines = linec-1#specifies the amount of lines
                break;#end the program
        elif(variable == "pgm"):
            section = "pgm"
            emptyc =0
        elif(variable == "var"):
            section = "var"
            emptyc = 0
        elif(variable == "const"):
            section = "const"
            emptyc = 0
        else:
            #retrieve the variable address
            emptyc = 0
            address = ""
            while(i<length):
                dbreak = False#sais if the loop should break
                #first it has to find the beginning of the word
                while(not(string[reallinec][i] == " " or string[reallinec][i] == "\t" or string[reallinec][i] == "\n")):
                    dbreak = True#the loop that goes throught the entire line should stop
                    if(string[reallinec][i] == "/"):
                        break
                    address = address+string[reallinec][i]
                    i = i+1
                if(dbreak):
                    break
                i = i+1
            #check if it is a valid address
            try:
                #it should be decoded differently depending if it is a hex a 
                #dec or a bin
                
                if(address[:2] == "0x"):
                    powe = 16
                elif(address[:2] == "0b"):
                    powe = 2
                else:
                    powe = 10
                valaddr = int(address, powe)
            except:
                print(address + "is an invalid address: line " + str(reallinec+1))
                exit()
            if(valaddr > 255 or 0 > valaddr):
                print("address " + address + " does not exist, you are only allowed to use address 0 too 255: line " + str(reallinec))
                exit()

            #check if the variable already exists
            try:
                var[0].index(variable)
            except:
                random = 1#this does nothing
            else:
                print(variable + " already exists: line " + str(reallinec+1))
                break
            
            #retrieve the value wich should be stored in the constant
            const = ""
            while(i<length):
                dbreak = False#sais if the loop should break
                #first it has to find the beginning of the word
                while(not(string[reallinec][i] == " " or string[reallinec][i] == "\t" or string[reallinec][i] == "\n")):
                    dbreak = True#the loop that goes throught the entire line should stop
                    if(string[reallinec][i] == "/"):
                        break
                    const = const+string[reallinec][i]
                    i = i+1
                if(dbreak):
                    break
                i = i+1   
            
            #put it in the list
            var[0].append(variable)
            var[1].append(str(bin(int(address,powe))))
            #test if the beginvalue is valid and if it is store it in the var list
            try:
                #depending if it is heximal, decimal or binary
                if(const[:2] == "0x"):
                    powe = 16
                elif(const[:2] == "0b"):
                    powe = 2
                else:
                    powe = 10
                var[2].append(str(bin(int(const, powe))))
            except:
                print("you have given an invalid beginvalue: line " + str(reallinec+1))
                exit()
            
        
        #store the address in variable list

    elif(section == "pgm"): #decoding program
        is_instruction = False#becomes true if there is an instruction on the line 
        label = False#becomes true if there is al label on the line
        f =True#its now entering the first loop of instruction finding
        a = False
        again = False
        while(f or a):#only if the loop is entered for the first time or it is said it should be done again
            f = False#when it has finished this loop it is not first loop anymore
            a = False#by default the loop shouldn't be done again
            bininstruct = 0    
            #first it has to find the instruction
            instruct = ""
            while(i<length):
                dbreak = False#sais if the loop should break
                #first it has to find the beginning of the word
                while(not(string[reallinec][i] == " " or string[reallinec][i] == "\t" or string[reallinec][i] == "\n")):
                    dbreak = True#the loop that goes throught the entire line should stop
                    if(string[reallinec][i] == "/"):
                        break
                    instruct = instruct+string[reallinec][i]
                    i = i+1
                if(dbreak):
                    break
                i = i+1
        
            skip = False #sais if the instruction is a skip instruction
            #decode the instruction
            
            c= False #this means that by default the program shouldn't continue
                     #decoding if it has finished decoding the instructions
            if(instruct == "pgm"):
                emptyc = 0

                #do nothing it is already in this mode
            elif(instruct == "const"):
                emptyc = 0
                section = "const"
            elif(instruct == "var"):
                emptyc = 0
                section = "var"#it changes the section where the program is in
            elif(not(instruct == "")): #skip this if there is nothing in it
                c = True
                emptyc = 0
                if(instruct == "load"):
                    is_instruction = True
                    bininstruct = 0
                elif(instruct == "store"):
                    is_instruction = True
                    bininstruct = 1
                elif(instruct == "and"):
                    is_instruction = True
                    bininstruct = 2
                elif(instruct == "not"):
                    is_instruction = True
                    bininstruct = 3
                elif(instruct == "add"):
                    is_instruction = True
                    bininstruct = 4
                elif(instruct == "neg"):
                    is_instruction = True
                    bininstruct = 5
                elif(instruct == "skip"):
                    is_instruction = True
                    skip = True
                    bininstruct = 6
                elif(instruct == "jmp"):
                    is_instruction = True
                    bininstruct = 7
                else:
                    a = True
                    label = True
                    
            else:
                if(label and not(is_instruction)):
                    print("The given instruction is invalid: line "+ str(reallinec+1))
                    exit()

        #the remainder of instruction should only be decoded if there 
        #is a valid instruction
        if(c):
            #try to find the remaining operands
            operand1 = ""
            if(skip):#skip is a special instruction so it has to decode in a different way
           
                #the first operand
                soperand1 = ""
                length = len(string[reallinec])
                while(i<length):
                    dbreak = False#sais if the loop should break
                    #first it has to find the beginning of the word
                    while(not(string[reallinec][i] == " " or string[reallinec][i] == "\t" or string[reallinec][i] == "\n")):
                        dbreak = True#the loop that goes throught the entire line should stop
                        if(string[reallinec][i] == "/"):
                            break
                        soperand1 = soperand1+string[reallinec][i]
                        i = i+1
                    if(dbreak):
                        break
                    i = i+1
                if  (soperand1 == "s"):
                    operand1 = "0010"
                elif(soperand1 == "z"):
                    operand1 = "1000"
                elif(soperand1 == "c"):
                    operand1 = "0100"
                else:
                    print(soperand1 + " is an invalid condition: line " + str(reallinec+1))
                    exit()

                #now it has to find the second operand only if the first was "s"
                if(soperand1 == "s"):
                    try:
                        #if(reallinec == 102):
                        soperand2 = ""
                        length = len(string[reallinec])
                        while(i<length):
                            dbreak = False#sais if the loop should break
                            #first it has to find the beginning of the word
                            while(not(string[reallinec][i] == " " or string[reallinec][i] == "\t" or string[reallinec][i] == "\n")):
                                dbreak = True#the loop that goes throught the entire line should stop
                                if(string[reallinec][i] == "/"):
                                    break
                                soperand2 = soperand2+string[reallinec][i]
                                i = i+1
                            if(dbreak):
                                break
                            i = i+1
                        operand2 = str(bin(int(soperand2)))
                    except:
                        print(soperand2 + " is an invalid operand: line " + str(reallinec+1))
                        exit()
                            
                    if(int(soperand2)>10 or int(soperand2)<0):
                        print("The bitaddress is not allowed to be bigger than 10 or smaller than 0: line " + str(reallinec+1))
                else:
                    operand2= "0b0"


                operand = ("0" * (4-len(operand2[2:]))+ operand2[2:] + operand1)            

            else:
                operand2 = ""#there is no 2nd operand
                soperand1 = ""
                length = len(string[reallinec])
                while(i<length):
                    dbreak = False#sais if the loop should break
                    #first it has to find the beginning of the word
                    while(not(string[reallinec][i] == " " or string[reallinec][i] == "\t" or string[reallinec][i] == "\n")):
                        dbreak = True#the loop that goes throught the entire line should stop
                        if(string[reallinec][i] == "/"):
                            break
                        soperand1 = soperand1+string[reallinec][i]
                        i = i+1
                    if(dbreak):
                        break
                    i = i+1
                if(ord(soperand1[0]) < 58 and 47 < ord(soperand1[0])):
                    #we know it is a number
                    try:
                        #it has to decode it in different way depending if the
                        #value is written in binary, decimal or hexadecimal
                        if(soperand1[:2] == "0x"):
                            powe = 16
                        elif(soperand1[:2] == "0b"):
                            powe = 2
                        else:
                            powe = 10
                        operand1 = str(bin(int(soperand1,powe)))
                    except:
                        print(soperand1 + " is an invalid operand: line " + str(reallinec+1))
                        exit()
                    if(int(soperand1[0]) > 255 and int(operand1[0]) < 0):
                        print("address " + soperand1 + " does not exist, you are only allowed to use address 0 too 255: line " + str(reallinec+1))
                        exit() 
                else:
                     try:
                        operand1 = var[1][var[0].index(soperand1)]
                     except:
                        try:
                            operand1 = bin(pvar[1][pvar[0].index(soperand1)])
                        except:
                            print("there is no variable \"" + soperand1 + "\", maybe you've put the variable in the wrong place: line " + str(reallinec+1))
                            exit()
                        
                operand = "0" * (8-len(operand1[2:])) + operand1[2:]
            program.append(["0b" + "0" *(3- len(str(bin(bininstruct))[2:])) + str(bin(bininstruct))[2:], operand, reallinec])
            linec = linec +1
    reallinec = 1 +reallinec#counts wich line of code we are
#write too the file
amlines = linec-1
i =0
wc = 0#counts how many times there has been written
logisim.write("v2.0 raw") #has to be at the beginnin of such a file
while(i<amlines):
    out.write(str(i)+"\t"+str(hex(i))+"\t" + "0x" + "0" * (3-len(str(hex(int(program[i][0]+program[i][1],2)))[2:])) + str(hex(int(program[i][0]+program[i][1],2)))[2:] + "\twas "+ str(program[i][2]+1) + string[program[i][2]])
    if(wc%8 == 0):
        logisim.write("\n")
    logisim.write(str(hex(int(program[i][0]+program[i][1],2)))[2:] + " ")
    i = i+1
    wc = 1+wc

#now it shall give a listing of the variables
out.write("\n\n\nList of variables\n\nname\taddress\tbeginvalue\n")
i = 0
while(i<len(var[0])):
    out.write(var[0][i] + "\t" + "0" * (8-len(var[1][i])) + var[1][i] + "\t" + "0" *(11-len(var[2][i][2:])) + var[2][i][2:] + "\n")
    i = 1+i
#now it shall store the variables in logisim
i = 0#the loop shall start at the highest address filling in everywhere it is necessary
find = amlines -1#the previous found value
while(not(i>255)):
    findl = find
    try:
        findin = var[1].index("0" * (8-len(str(bin(i)))) + str(bin(i)))
    except:
        #now it doesn't have to do anything
        random = 33.2439820349342039849298398492-1
    else:
        find = i
        if(int(var[1][findin],2) <= amlines-1):#it overlaps with program
            print("variable " + var[0][findin] + " overlaps with the program")
            exit()
        #now it has to print out how many zeros are between the newly discovered
        #value and the last discovered
        wc = wc +1
        if(not(find-findl==0)):#there is no point writing how many zeros there where if there where none
            logisim.write(str(find-findl-1) + "*0 ")
            if(wc%8 == 0):
                logisim.write("\n")
        #write the newly found one
        wc = wc +1
        logisim.write(str(hex(int(var[2][findin],2)))[2:] + " ")
    i = i +1
out.close()
logisim.close()
