import sys,os

DATA = sys.argv[1]

def write_style(o):
	o.write('<style type="text/css">\n')
	o.write('table { margin: 1em; border-collapse: collapse; }\n')
	o.write('td, th { padding: .3em; border: 1px #ccc solid; }\n')
	o.write('thead { background: #fc9; cursor:pointer;cursor:hand; } \n')
	o.write('</style>\n')

def write_header(o):
	o.write('<html><head><script src="sorttable.js"></script>\n')
	write_style(o)
	o.write('</head><body>\n')

def generate_chart(i, o, name = None, width = 1000, height = 300, leg = []):
	if not isinstance(i, list):
		i = [i]
	print "Generating", o, i
	if leg == []:
		legend = []
		for c in i:
			f = open(c, "r")
			line = f.readline().split(',')
			if (len(line) < 2):
				return;
			legend += [line[1][:-1]];
			f.close()
	else:
		legend = leg
	f = open(".temp.r", "w")
	for index in range(len(i)):
		f.write('d' + str(index) + ' <- read.table("' + i[index] + '", sep=",", header=TRUE)\n')

	f.write('png("' + o + '", width=' + str(width) + ', height=' + str(height) + ')\n')
	f.write('matplot(d0[1],cbind(')

	for index in range(len(i)):
		f.write('d' + str(index) + '[2]')
		if index + 1 != len(i):
			f.write(',');
	if not name:
		name = i[0]
	f.write('),type="l",lty=c(1),col=c("blue","red","green"), xlab="Time", ylab="Watts", main="' + name + '")\n')

	f.write('legend("topright",c(')
	for index in range(len(i)):
		f.write('"' + legend[index] + '"')
		if index + 1 != len(i):
			f.write(',');

	f.write('), lty=c(1,1),lwd=c(2.5,2.5),col=c("blue","red","green"))\n')
	f.write('dev.off()\n')
	f.write('q()\n');
	f.close()

	os.system("R --no-save < .temp.r >/dev/null")

def get_test_info(i):
	info = {}
	f = open(i, "r")
	line = f.readline().split(',')
	if (len(line) < 2):
		return;

	info['component'] = os.path.basename(i[:i.find("-")])
	info['name'] = line[1]

	lines = f.readlines()
	info['samples'] = len(lines);

	average = 0.0
	energy = 0.0
	for line in lines:
		l = line.split(',')
		average += float(l[1])
		energy += 0.2 * float(l[1]);
	average = average / len(lines)
	info['average'] = average
	info['energy'] = energy
	f.close()
	return info

def write_test_header(i, o):
	f = open(i, "r")
	line = f.readline().split(',')
	if (len(line) < 2):
		return;

	o.write("Name: " + line[1] + "<br/>")

	lines = f.readlines()
	o.write("Samples: " + str(len(lines)) + "<br/>")

	average = 0.0
	energy = 0.0
	for line in lines:
		l = line.split(',')
		average += float(l[1])
		energy += 0.2 * float(l[1]);
	average = average / len(lines)
	o.write("Average: " + str(average) + "<br/>")
	o.write("Energy: " + str(energy) + "<br/>")
	o.write('Data: <a href="' + os.path.basename(i) + '">' + os.path.basename(i) + '</a><br/>')
	f.close()

def write_component_table(inp, o):
	o.write('<table class="sortable" style="border: 1px black solid"><tr><th>Test</th><th>Watts</th><th>Energy</th></tr>\n')
	for i in inp:
		info = get_test_info(i)
		o.write('<tr><td>' + info['name'] + '</td><td>' + str(info['average']) + '</td><td>' + str(info['energy']) + '</td></tr>\n')
	o.write("</table>")

def write_test_table(inp, o):
	o.write('<table class="sortable" style="border: 1px black solid"><tr><th>Component</th><th>Watts</th><th>Energy</th></tr>\n')
	for i in inp:
		info = get_test_info(i)
		o.write('<tr><td>' + info['component'] + '</td><td>' + str(info['average']) + '</td><td>' + str(info['energy']) + '</td></tr>\n')
	o.write("</table>")


def average_tests(i1, i2, index):
	if not os.path.exists(i1):
		f = open(i1, "w")
		f.close()
	f1 = open(i1, "r")
	f2 = open(i2, "r")

	f1.readline()
	data = f2.readline()

	lines1 = f1.readlines()
	lines2 = f2.readlines()

	if len(lines2) == 0:
		f1.close()
		f2.close()
		return;

	if len(lines1) == 0:
		lines1 = lines2

	for i in range(max(len(lines1), len(lines2))):
		line1 = lines1[i].split(',')
		line2 = lines2[i].split(',')
		data += line1[0] + "," + str((float(line1[1]) * index + float(line2[1])) / (index + 1)) + "\n"

	f1.close()
	f2.close()

	f1 = open(i1, "w")
	f1.write(data)
	f1.close()

def generate_components_html():
	index_html = open(DATA + "/components.html", "w")
	write_header(index_html)
	index_html.write("<h1>Per component results</h1>\n")

	current_test_name = ""
	current_test_html = None
	current_test_average_index = 1
	current_component_name = ""
	current_component_html = None
	all_in_one = []

	files = os.listdir(DATA)
	files.sort()
	for csv in files:
		if not csv[-1].isdigit() and not csv.endswith("energy"):
			continue

		if current_component_name != csv[:csv.find("-")]:
			if all_in_one != []:
				index_html.write('<h3>' + current_component_name + ' - all in one</h3>\n');
				write_component_table(all_in_one, index_html)
				index_html.write('<a href="' + current_component_name + ".html" + '"> - Show details</a><br/>')
				index_html.write('<img src="' + current_component_name + '.png"/><br/>\n')
				generate_chart(all_in_one, DATA + "/" + current_component_name + ".png", current_component_name, height = 300)
			all_in_one = []
			generate = len(current_component_name) != 0
			current_component_name = csv[:csv.find("-")]
			if current_component_html:
				current_test_html.write("</body></html>\n")
				current_test_html.close()
				write_test_header(DATA + current_test_name + ".csv.average", current_component_html)
				current_component_html.write('<img src="' + current_test_name + ".csv.average.png" + '"/><br/>\n')
				generate_chart(DATA + current_test_name + ".csv.average", DATA + current_test_name + ".csv.average.png", height = 300)
				current_test_html = None
				current_component_html.write("</body></html>\n")
				current_component_html.close()
			current_component_html = open(DATA + "/" + current_component_name + ".html", "w")
			current_component_html.write('<html><head><script src="sorttable.js"></script></head><body>\n')


		if current_test_name != csv[:csv.find(".")]:
			if current_test_html:
				current_test_html.write("</body></html>\n")
				current_test_html.close()
				write_test_header(DATA + current_test_name + ".csv.average", current_component_html)
				current_component_html.write('<img src="' + current_test_name + ".csv.average.png" + '"/><br/>\n')
				generate_chart(DATA + current_test_name + ".csv.average", DATA + current_test_name + ".csv.average.png", height = 300)
			#if all_in_one == []:

			current_test_html = open(DATA + "/" + csv[:csv.find(".")] + ".html", "w")
			current_test_html.write("<html><head></head><body>\n")
			current_test_name = csv[:csv.find(".")]
			current_test_average_index = 1
			os.system('rm -f "' + DATA + current_test_name +'.csv.average"')
			current_component_html.write('<h3>' + current_test_name + '</h3>\n');
			current_component_html.write(' - <a href="' + csv[:csv.find(".")] + ".html" + '">All measurements</a><br/><br/>\n');
			all_in_one += [DATA + current_test_name + ".csv.average"]

		if csv[-1].isdigit():
			generate_chart(DATA + "/" + csv, DATA + "/" + csv + ".png")
			write_test_header(DATA + "/" + csv, current_test_html)
			average_tests(DATA + current_test_name + ".csv.average", DATA + "/" + csv, current_test_average_index)
			current_test_average_index += 1
			current_test_html.write('<img src="' + csv + ".png" + '"/><br/><hr/>\n')


	index_html.write('<h3>' + current_component_name + ' - all in one</h3>\n');
	write_component_table(all_in_one, index_html)
	index_html.write('<a href="' + current_component_name + ".html" + '"> - Show details</a><br/>')
	index_html.write('<img src="' + current_component_name + '.png"/><br/>\n')
	generate_chart(all_in_one, DATA + "/" + current_component_name + ".png", current_component_name, height = 300)

	write_test_header(DATA + current_test_name + ".csv.average", current_component_html)
	current_component_html.write('<img src="' + current_test_name + ".csv.average.png" + '"/><br/>\n')
	generate_chart(DATA + current_test_name + ".csv.average", DATA + current_test_name + ".csv.average.png", height = 300)

	generate_chart(all_in_one, DATA + "/" + current_component_name + ".png", current_component_name, height = 300)

	current_test_html.write("</body></html>\n")
	current_test_html.close()

	current_component_html.write("</body></html>\n")
	current_component_html.close()

	#generate_chart(DATA + current_test_name + ".csv.average", DATA + current_test_name + ".csv.average.png")
	#index_html.write('<img src="' + current_test_name + ".csv.average.png" + '"/><br/>\n')

	index_html.write("</body></html>\n")
	index_html.close()

def generate_tests_html():
	index_html = open(DATA + "/tests.html", "w")
	write_header(index_html)
	index_html.write("<h1>Per test results</h1>\n")

	files = os.listdir(DATA)
	files.sort()
	components = []
	tests = []
	for csv in files:
		if not csv.endswith(".average"):
			continue
		component = csv[:csv.find("-")]
		if not component in components:
			components += [component]
		test = csv[csv.find("-") + 1 : csv.find(".")]
		if not test in tests:
			tests += [test]

	for t in tests:
		tmp = []
		used = []
		for c in components:
			f = DATA + "/" + c + "-" + t + ".csv.average"
			if os.path.exists(f):
				tmp += [DATA + "/" + c + "-" + t + ".csv.average"]
				used += [c]
		index_html.write('<h3>' + get_test_info(tmp[0])['name'] + '</h3>\n');
		write_test_table(tmp, index_html)
		index_html.write('<img src="' + t + '.png"/>\n')
		generate_chart(tmp, DATA + "/" + t + ".png", t, height = 300, leg = used)

	index_html.write("</body></html>\n")
	index_html.close()

def generate_index_html():
	index_html = open(DATA + "/index.html", "w")
	write_header(index_html)
	index_html.write("<h1>Measurement results</h1>\n")

	index_html.write('- <a href="components.html">Per component results</a><br/>\n')
	index_html.write('- <a href="tests.html">Per test results</a><br/>\n')

	index_html.write("</body></html>\n")
	index_html.close()

os.system("cp sorttable.js " + DATA + "/sorttable.js")
generate_components_html()
generate_tests_html()
generate_index_html()

