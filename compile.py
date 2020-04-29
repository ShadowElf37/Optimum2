import re
import errors
import tokenize
import build
import parse
from op_literals import CodeBlock

STD = [
    'from _lib import *',
]

def compile(block, scope='GLOBAL'):
    tokenized = []

    block = re.sub('\s+', ' ', block)

    # Strip all comments
    block = re.sub('//[^\n]*\n', '', block)
    block = parse.StatefulParser('/*', '*/').purge(block)
    codeblocks = parse.StatefulParser('{', '}').match(block, nestlimit=1, include_delimiter=True)[1]
    for cb in codeblocks:
        block = block.replace(cb, cb.replace(';', '::'))
    # print(block)

    block = re.split(';', block)
    for lineno, statement in enumerate(block):
        try:
            tokenized.append(tokenize.resolve(statement.strip()))
        except errors.CompilerError as e:
            raise e.again(' (Line %s)' % (lineno+1)) from None

    built = []
    for chain in tokenized:
        constructed = build.build(chain, compiler=compile, scope=scope)
        if constructed is not None:
            built.append(constructed.replace('\t', '    '))

    return built

if __name__ == "__main__":
    cmp = compile(open('test.o').read())

    print('\n'.join(STD))
    print()
    print('\n'.join(CodeBlock.DEFINITIONS))
    print('\n'.join(cmp))