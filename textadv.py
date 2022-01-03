import sys

class Item:
	def __init__(self, name, desc, use = lambda: None, gettable = True):
		self.desc = desc
		self.name = name
		self.use = use
		self.gettable = gettable

class Room:
	def __init__(self, desc, handler = lambda cmd: False):
		self.desc = desc
		self.exits = {}
		self.items = {}
		self.handler = handler

	def __str__(self):
		return self.desc + " " + str(self.exits)

	def add_exit(self, dir, room):
		self.exits[dir] = room
		return self

	def add_item(self, name, item):
		self.items[name] = item
		return self
	def get_desc(self):
		desc = "You are in "+self.desc
		for item in self.items:
			desc+=" "+self.items[item].name
		return desc

items = {}
rooms = []
room = None

def locked_room_handler(cmd):
	global room
	if cmd=="go east":
		if "key" in items:
			room=rooms[room.exits["east"]]
			print(room.get_desc())
		else:
			print("Sorry you can't go through a locked door. maybe if you had a key...")
		return True
	else:
		return False

def use_portal():
	print("Yay you beat level ZERO good job (:")
	exit(0)

rooms += [Room("a room that is fairly small. there is a door to the east.", locked_room_handler).add_exit("east", 1).add_item("key",Item("There is a key on a small table.", "you find a key which seems to unlock a door"))]
rooms += [Room("a abnormally large room, there is a door to the west.").add_exit("west", 0).add_item("portal", Item("There is a portal in the center of the room","A mysterious portal that looks like it leads to another room.", use_portal, False))]
room = rooms[0]


print(room.get_desc())

for cmd in sys.stdin:
	cmd=cmd.lower().strip()
	if room.handler(cmd):
		continue
	elif cmd == "yell":
		print("AHHHHHHHH DAT CREEPY")
	elif cmd == "exit":
		break
	elif cmd == "look":
		print(room.get_desc())
	elif cmd.startswith("look "):
		words=cmd.split(" ", 1)
		if words[1] in room.items:
			print(room.items[words[1]].desc)
		elif words[1] in items:
			print(items[words[1]].desc)
		else:
			print("you can't see that.!")
	elif cmd.startswith("go "):
		words=cmd.split(" ", 1)
		if words[1] in room.exits:
			room=rooms[room.exits[words[1]]]
			print(room.get_desc())
		else:
			print("You Can't Go There, Sorry: "+words[1])
	elif cmd.startswith("get "):
		words=cmd.split(" ", 1)
		if words[1] in room.items and room.items[words[1]].gettable:
			items[words[1]] = room.items[words[1]]
			del room.items[words[1]]
			print("you picked up the "+ words[1])
		else:
			print("NOPE! SORRY!")
	elif cmd.startswith("use "):
		words=cmd.split(" ", 1)
		if words[1] in room.items:
			room.items[words[1]].use()
		else:
			print("NOPE! SORRY!")
	elif cmd == "inv":
		for item in items:
			print(item)
	else:
		print("unknown command try again: "+cmd)
print("Goodbye have fun!")