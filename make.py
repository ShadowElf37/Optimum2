import sys
from compile import compile, STD, CodeBlock

stdout = sys.stdout

print('Compiling...')
sys.stdout = None

with open(sys.argv[1], 'r') as file:
    f = file.read()

cmp = '\n'.join(compile(f))
std = '\n'.join(STD)
obj = '\n'.join(CodeBlock.DEFINITIONS)

with open(sys.argv[2], 'w') as dest:
    dest.write('\n'.join((std, obj, cmp)))

sys.stdout = stdout
print('Done.')