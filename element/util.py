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

def coords(t):
    return ((t[0] + 4000) / 10.0, (t[2] + 5500) / 10.0, t[1] / 10.0)

def Regions(filename):
    with open(filename) as f:
        things = []
        lines = parse_token_file(f.read()[2:].decode('utf_16_le'))
        i = 2
        used_ids = set() # Because we can have duplicates o.o
        q = collections.namedtuple('RegionParams', ('id', 'coord_count', 'waypoint_count', '?','?', 'music_count', '?', '?', '?', '?'), rename=True)
        p = collections.namedtuple('Point', ('x','y','z'))
        r = collections.namedtuple('Region', ('id', 'name', 'home_point', 'vertices', 'waypoints'))
        while i < len(lines):
            name = lines[i][0]
            params = q._make(int(x) for x in lines[i+1])
            home_point = p(*coords([float(x.rstrip(',')) for x in lines[i+2]]))
            waypoints = {}
            points = []
            i += 3
            for j in xrange(int(params.coord_count)):
                points.append(p(*coords([float(x) for x in lines[i]])))
                i += 1
            if points[0] != points[-1]:
                points.append(points[0])
            for j in xrange(int(params.waypoint_count)):
                waypoints[lines[i][0]] = p(*coords([float(x) for x in lines[i][1:]]))
                i += 1
            i += 2 + params.music_count
            if params.id not in used_ids:
                waypoints = {}
                used_ids.add(params.id)
            things.append(r(params.id, name, home_point, points, waypoints))

        return things

            
