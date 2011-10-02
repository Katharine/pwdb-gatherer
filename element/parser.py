#encoding=utf8
import struct
from collections import namedtuple

def get_type_length(t):
	lens = {
		'int16': 2,
		'int32': 4,
		'int64': 8,
		'float': 4,
		'double': 8
	}
	if t in lens:
		return lens[t]
	elif t[0:4] == 'byte':
		if t == 'byte:AUTO':
			raise Exception, "byte:AUTO is not real!"
		return int(t[5:])
	elif t[0:7] == 'wstring':
		return int(t[8:])
	elif t[0:6] == 'string':
		return int(t[7:])
	else:
		return 0

def get_struct_str(t):
	if t == 'int16':
		return 'H'
	elif t == 'int32':
		return 'I'
	elif t == 'int64':
		return 'Q'
	elif t == 'float':
		return 'f'
	elif t == 'double':
		return 'd'
	elif t[0:4] == 'byte':
		return '%ss' % t[5:]
	elif t[0:7] == 'wstring':
		return '%ss' % t[8:]
	elif t[0:6] == 'string':
		return '%ss' % t[7:]

class ElementList(object):
	def __init__(self, elements, offset, labels, types, entry_length):
		self.elements = elements
		self.offset = offset
		with open(elements) as f:
			f.seek(offset)
			self.length = struct.unpack('<I', f.read(4))[0]
		self.offset += 4
		self.labels = labels
		self.types = types
		self.entry_length = entry_length
		self.tuple = namedtuple('ElementItem', self.labels, rename=True)
	
	def __len__(self):
		return self.length
	
	def __repr__(self):
		return '[%s]' % ', '.join(x.__repr__() for x in self)
	
	def __str__(self):
		return '[%s]' % ', '.join(str(x) for x in self)

	def __getitem__(self, key):
		if not isinstance(key, int) and not isinstance(key, slice):
			raise TypeError
		if isinstance(key, slice):
			return [self.__getitem__(x) for x in key.indices(self.length)]
		if key < 0:
			key = self.length - key
		if key >= self.length:
			raise IndexError
		offset = self.offset + self.entry_length * key
		with open(self.elements) as f:
			f.seek(offset)
			struct_str = ''.join([get_struct_str(x) for x in self.types])
			t = list(struct.unpack('<%s' % struct_str, f.read(self.entry_length)))
			for i in xrange(len(self.types)):
				if self.types[i][0:7] == 'wstring':

					t[i] = t[i].decode('utf_16_le').rstrip('\x00')
				elif self.types[i][0:6] == 'string':
					t[i] = t[i].decode('gbk').rstrip('\x00')
			return self.tuple(*t)


class ElementParser(object):
	def __init__(self, elements, config):
		self.elements = elements
		self.config_file = config
		self.config = {}
		self.offsets = []
		self.parse_config_file()
	
	def get_list_entry_length(self, types, current_id=None, current_offset=None):
		length = 0
		for t in types:
			if t == 'byte:AUTO':
				# This is both retarded and really, really slow. D:<
				offset = self.get_list_offset((current_id, current_offset))
				pattern = "facedata\\"
				byte_len = -72-len(pattern)
				run = True
				with open(self.elements) as f:
					f.seek(offset)
					while run:
						run = False
						for i in xrange(len(pattern)):
							byte_len += 1
							if f.read(1) != pattern[i]:
								run = True
								break
				length += byte_len
			else:
				length += get_type_length(t)
		return length

	def get_list_offset(self, l):
		if isinstance(l, tuple):
			list_id = l[0]
			list_offset = l[1]
		else:
			list_id = self.config[l][0]
			list_offset = self.config[l][1]
		with open(self.elements) as f:
			for i in xrange(list_id):
				f.seek(self.offsets[i][0], 1)
				if i == 58:
					length = 1
				else:
					length = struct.unpack('<I', f.read(4))[0]
				f.seek((length) * self.offsets[i][1], 1)
			f.seek(list_offset, 1)
			return f.tell()

	def parse_config_file(self):
		with open(self.config_file) as f:
			list_count = int(f.readline().strip())
			current_id, current_name, current_offset, current_labels, current_types = None, None, None, None, None
			while True:
				line = f.readline()
				if not line:
					break
				line = line.strip()
				if not line or line[0] == '#':
					continue
				if current_id is None:
					id_str, label = line.split('-', 1)
					current_id = int(id_str.strip()) - 1
					current_name = label.strip().lower().replace(' ','_')
				elif current_offset is None:
					current_offset = int(line)
				elif current_labels is None:
					current_labels = [x.lower().replace(' ', '_') for x in line.split(';')]
				elif current_types is None:
					current_types = line.split(';')
					# We're done!
					self.offsets.append((current_offset, self.get_list_entry_length(current_types, current_id, current_offset)))
					self.config[current_name] = (current_id, current_offset, current_labels, current_types)
					current_id, current_name, current_offset, current_labels, current_types = None, None, None, None, None
	
	def get_list(self, name):
		offset = self.get_list_offset(name)
		entry_length = self.offsets[self.config[name][0]][1]
		labels = self.config[name][2]
		types = self.config[name][3]
		return ElementList(self.elements, offset, labels, types, entry_length)

	def __getattr__(self, attr):
		if attr in self.config:
			return self.get_list(attr)
		else:
			raise AttributeError, "'ElementParser' object has no attribute '%s'" % attr
