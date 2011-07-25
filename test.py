import sys
import time
import telnetlib

HOST = sys.argv[1]
PORT = sys.argv[2]
COUNT = int(sys.argv[3])
TIME = int(sys.argv[4])
OUT = sys.argv[5]
NAME = sys.argv[6]

def measure_once(out, t):
	f = open(out, "w")

	tn = telnetlib.Telnet(HOST,PORT)

	for i in range(10):
		print "starting in", 10 - i
		time.sleep(1)

	tn.write("Go,200,10\n")
	print "started"

	tn.read_until("\n")
	t -= 1

	while t:
		print "measuring -", t, "seconds left"
		t -= 1
		time.sleep(1)

	print "sleeping for 2 seconds to be sure to have enough samples"
	time.sleep(2)

	tn.write("w\n")
	tn.write("S\n")

	print "stopped, waiting for data"
	data = tn.read_until("\n")

	print "analyzing"
	energy = 0.0
	splitted = data.split(",")
	print "received", len(splitted[2:]), "samples"
	print "only", TIME * 5, "samples will be used"
	splitted = splitted[:TIME * 5]
	f.write("Time," + NAME + "\n")
	i = 0.0;
	for value in splitted[2:]:
		energy += 0.2 * float(value)
		f.write(str(i) + "," + value + "\n")
		i += 0.2;
	print "Total energy consumed:", energy, "J"
	f.close()
	print "done"
	return energy


for i in range(1,COUNT + 1):
	raw_input("press Enter once you will be ready to start")
	print "Starting measurement number", i
	print "Output file is", OUT + "." + str(i), "and", OUT + "." + str(i) + ".energy"
	energy = measure_once(OUT + "." + str(i), TIME)
	f = open(OUT + "." + str(i) + ".energy", "w")
	f.write(NAME + "\n")
	f.write(str(energy) + "\n")
	f.close()

