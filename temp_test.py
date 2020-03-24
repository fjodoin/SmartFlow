import sys

while True:
	try:
		print("waiting...")
		data = sys.stdin.readline()
	except KeyboardInterrupt:
		break
	if not data:
		break
	print(data)