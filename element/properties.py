def ItemProperties(filename):
	content = open(filename).read().decode('gbk')
	char = content[0]
	next = content[1]
	state = 'none'
	token = ''
	current_type = None
	output = {}
	for i in xrange(len(content)):
		char = content[i]
		next = content[i+1] if i+1 < len(content) else ''
		if state == 'multicomment':
			if char == '*' and next == '/':
				state = 'none'
		elif state == 'singlecomment':
			if char in '\r\n':
				state = 'none'
		elif state == 'none':
			if char == '/' and next == '*':
				state = 'multicomment'
			elif char == '/' and next == '/':
				state = 'singlecomment'
			elif char == '{':
				state = 'grouping'
			elif char not in '\r\n':
				token += char
				if next in '\r\n\t:, ':
					if token == 'type' and next == ':':
						state = 'type_num'
					else:
						print "Discarding token '%s'." % token
					token = ''
		elif state == 'type_num':
			if char not in ' \t\r:':
				token += char
				if next not in '0123456789':
					state = 'none'
					current_type = int(token)
					token = ''
		elif state =='grouping':
			if char == '}':
				if token != '' and current_type is not None:
					output[int(token)] = current_type
				token = ''
				current_type = None
				state = 'none'
			elif char == ',':
				if current_type is not None:
					output[int(token)] = current_type
				token = ''
			elif char not in '\r\n\t ':
				token += char
	return output
