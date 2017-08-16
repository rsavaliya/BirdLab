import re, math, argparse, os

parser = argparse.ArgumentParser()
parser.add_argument("infile", help = "Run program on given folder with file path")
parser.add_argument("-d" , type = float, default = .1, help = "Give max difference between measurements in cm (Default = .1cm)")
args = parser.parse_args()

os.chdir(args.infile)
name = raw_input("Enter name 1: ")
name2 = raw_input("Enter name 2: ")
lm = int(raw_input("Enter number of landmarks: "))

rishi = open(name + "/combined_landmarks.txt", "r")
salman = open(name2 + "/combined_landmarks.txt", "r")
w = open("Differences.txt", "w")
w2 = open("Fixes.txt", "w")
rishi = rishi.readlines()
salman = salman.readlines()
rbirds = {}
sbirds = {}

i = 0
while i < len(rishi):
    scale = float(rishi[i+lm+2][6:].strip())
    acc = int(re.search(r'\d+', rishi[i+lm+1]).group())
    points = []
    j = 0
    while j != lm:
        points.append(rishi[i+j+1].strip().split())
        j += 1
    points.append(scale)
    rbirds[acc] = points
    i+=lm+3

i = 0
while i < len(salman):
    scale = float(salman[i+lm+2][6:].strip())
    acc = int(re.search(r'\d+', salman[i+lm+1]).group())
    points = []
    j = 0
    while j != lm:
        points.append(salman[i+j+1].strip().split())
        j += 1
    points.append(scale)
    sbirds[acc] = points
    i+=lm+3

matches = list(set(rbirds) & set(sbirds))

for b in matches:
    star = []
    w.write("BIRD = " + str(b) + "\n")
    i = 0
    avgsc = ((rbirds[b][lm]) + (sbirds[b][lm]))/2
    while i < lm:
        point1 = rbirds[b][i]
        point2 = sbirds[b][i]
        x = int(point1[0]) - int(point2[0])
        y = int(point1[1]) - int(point2[1])
        diff = math.sqrt(x*x + y*y)
        if avgsc*diff > args.d: 
            w.write("LANDMARK " + str(i+1) + " DIFFERENCE: " + str(diff) + " px **\n")
            star.append("LANDMARK " + str(i+1) + " DIFFERENCE: " + str(diff) + " px\n")
        else: w.write("LANDMARK " + str(i+1) + " DIFFERENCE: " + str(diff) + " px\n")
        i += 1
    w.write(name + " scale: " + str(1/rbirds[b][lm]) + " px/cm\n")
    w.write(name2 + " scale: " + str(1/sbirds[b][lm]) + " px/cm\n")
    w.write("Average scale: " + str(1/avgsc) + " px/cm\n")
    w.write("Difference in scales: " + str(abs((1/rbirds[b][lm]) - (1/sbirds[b][lm]))) + " px/cm\n")
    w.write("\n")
    if len(star) != 0:
        w2.write("BIRD = " + str(b) + "\n")
        w2.writelines(star)
        w2.write("\n")
        w2.write(name + " scale: " + str(1/rbirds[b][lm]) + " px/cm\n")
        w2.write(name2 + " scale: " + str(1/sbirds[b][lm]) + " px/cm\n")
        w2.write("Average scale: " + str(1/avgsc) + " px/cm\n")
        w2.write("Difference in scales: " + str(abs((1/rbirds[b][lm]) - (1/sbirds[b][lm]))) + " px/cm\n")
        w2.write("\n")
        w2.write("\n")

w.close()
w2.close()

print(str(len(matches)) + " birds were similar between these two people")