import collections

# This will probably fail if a line ends with "/" and the following line starts with "/".
def parse_token_file(content, token_sep=' \t', line_sep='\r\n', quote='"'):
	lines = []
	line = []
	token = ''
	in_quote = False
	in_comment = False
	last_char = ''
	for char in content:
		if not in_comment:
			if in_quote:
				if char == quote:
					in_quote = False
					line.append(token.replace("\\r", "\n").replace("\r\n","\n").replace("\r","\n"))
					token = ''
				else:
					token += char
			else:
				if char == quote:
					in_quote = True
				elif char == '#':
					in_comment = True
				elif char == '/' and last_char == '/':
					token = token[:-1]
					in_comment = True
				elif char in token_sep:
					if token != '':
						line.append(token.replace("\\r", "\n").replace("\r\n","\n").replace("\r","\n"))
					token = ''
				elif char in line_sep:
					if token != '':
						line.append(token.replace("\\r", "\n").replace("\r\n","\n").replace("\r","\n"))
						token = ''
					if len(line) != 0:
						lines.append(line)
						line = []
				else:
					token += char
		else:
			if char in line_sep:
				in_comment = False
		last_char = char
	if token != '':
		line.append(token.replace("\\r", "\n").replace("\r\n","\n").replace("\r","\n"))
	if len(line) != 0:
		lines.append(line)
	return lines

def ElementDescriptions(filename):
	with open(filename) as f:
		content = f.read()[2:].decode('utf_16_le')
		lines = parse_token_file(content)
		descriptions = {}
		for line in lines:
			descriptions[int(line[0])] = line[1]
		return descriptions

def ElementColours(filename):
	with open(filename) as f:
		content = f.read()
		lines = parse_token_file(content)
		colours = {}
		for line in lines:
			colours[int(line[0])] = int(line[1])
		return colours

def ElementSkills(filename):
	with open(filename) as f:
		content = f.read()[2:].decode('utf_16_le')
		lines = parse_token_file(content)
		skills = {}
		t = collections.namedtuple('ElementSkill', ('id', 'name', 'description'))
		for i in xrange(0, len(lines), 2):
			skills[int(lines[i][0])/10] = t(int(lines[i][0])/10, lines[i][1], lines[i+1][1])
		return skills

def SpawnLocations(filename):
	with open(filename) as f:
		f.readline() # We don't care about the header.
		content = f.read().decode('gbk')
		lines = parse_token_file(content)
		spawns = {}
		t = collections.namedtuple('SpawnPoint', ('map', 'x', 'y', 'z'))
		for line in lines:
			try:
				spawn = int(line[0])
				if spawn not in spawns:
					spawns[spawn] = []
				spawns[spawn].append(t(line[1], (float(line[2]) + 4000)/10.0, (float(line[4]) + 5500)/10.0, (float(line[3]) / 10.0)))
			except (ValueError):
				pass
		return spawns
