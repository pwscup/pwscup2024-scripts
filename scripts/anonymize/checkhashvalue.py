import sys, hashlib

if len(sys.argv) != 2:
	print(f"Usage: python checkhashvalue.py <filename>")
	sys.exit(1)

fn = sys.argv[1]
f = open(fn, 'r')
data = f.read()
f.close()

hv = hashlib.sha256(data.encode()).hexdigest()

print(hv)

