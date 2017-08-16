import argparse, glob, os, re
 
parser = argparse.ArgumentParser()
parser.add_argument("infile", help = "Run program on given folder with file path")
#parser.add_argument("--outfile", '-o', help = "Specify the output file name", required = True)
args = parser.parse_args()
 
os.chdir(args.infile)
name = raw_input("Gurllll what's your name? ") #Asks for yo gurl's name
LM_input = input("How many landmarks does your bird have? ") #user enters number of landmarks for bird ##########SALMAN##########
tail = LM_input + 7 ##########SALMAN##########
tail = int(tail) #End point for gathering LM's into the head [] ##########SALMAN##########
 
counter = 0
files = []
for something in glob.glob("*.txt"):
    files.append(something)
files = [x for x in files if not x.startswith("combined")]

w = open("combined_landmarks.txt", 'w') #creates the output file in the folder
#w = open(args.outfile + ".txt" , 'w') #open write file

for bird in files: #goes through all the files
    r = open(bird, 'r')
    head = [next(r).strip() for x in xrange(tail)] #gets top [tail] lines in file
    if ("square" in head[1]) or ("scaling" not in head[4]):
        print(bird + " has invalid or no scale!")
        LM = 999
    else:
        pos = head[5].find('nrow=')
        LM = int(head[5][pos+5:pos+7]) #gets the number of landmarks
    if LM == LM_input: #only works if landmark number is same as what you input at beginning
        i = 6
        landmarks = []
        while i < tail - 1:
            landmarks.append(head[i].strip())
            i += 1
        lmlist = []
        for x in landmarks: #create list of all the landmarks
            lmlist.append(x.split('\t'))
        pos = head[4].find('numeric')
        scale = re.findall(r'[+-]?[0-9.]+', head[4][45:])
        scale = float(scale[0]) #get the scale
         
        w.write("LM = " + str(LM_input) + "\n") #writes all to file
        for x in lmlist:
            w.write(x[1] + '\t' + x[2] + '\n')
        w.write("IMAGE=" + name + "_" + bird + '\n')
        w.write("SCALE=" + str(scale) + '\n')
        counter += 1
    elif LM < LM_input: print(bird + " did not have enough landmarks.")
    else: pass
w.close()
r.close()

print("Total number of birds landmarked: " + str(counter))