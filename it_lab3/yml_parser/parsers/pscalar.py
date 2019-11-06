import re

re_scalar = re.compile(r'(\w*?)\s*(.*)', re.DOTALL)

def parse_scalar(src):
        match = re_scalar.match(src)
        if match is not None:
                scalar, src = match.groups()
                yield eval(scalar), src

for i in parse_scalar('time vector clang\n'):
        print(i)
