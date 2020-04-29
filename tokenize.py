import re
import errors
from parse import StatefulParser

class Group:
    def __init__(self, name, text):
        self.name = name
        self.text = text

    def build(self):
        return self.name + ', ' + self.text


TOKENIZATION_RULES = {
    'KEYWORD': re.compile(r'let|is|of|return|for|while|in|true|false|null|undefined|unpack|from|if|import|puts|try|catch|else|with'),
    'NAME': re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*'),
    'INAME': re.compile(r'^\.[a-zA-Z_][a-zA-Z0-9_]*'),
    'CLASS': re.compile(r'\$'),

    'INT': re.compile(r'\d+'),
    'FLOAT': re.compile(r'(\d*\.\d+)|(\d+\.\d*)'),
    'STRING': re.compile(r'[\'"][^\'"]*[\'"]'),

    'OP_EQ': re.compile(r'='),
    'OP_ADD': re.compile(r'\+'),
    'OP_SUB': re.compile(r'-'),
    'OP_MUL': re.compile(r'\*'),
    'OP_DIV': re.compile(r'/'),
    'OP_MOD': re.compile(r'%'),
    'OP_INC': re.compile(r'\+\+'),
    'OP_DEC': re.compile(r'--'),
    'OP_FORCE': re.compile(r'!'),
    'CMP_EQ': re.compile(r'=='),
    'CMP_GT': re.compile(r'>'),
    'CMP_LT': re.compile(r'<'),
    'CMP_GE': re.compile(r'>='),
    'CMP_LE': re.compile(r'<='),

    'COMMA': re.compile(r','),
    'OPEN_PAR': re.compile(r'\('),
    'CLOSE_PAR': re.compile(r'\)'),
    'OPEN_BRACKET': re.compile(r'\['),
    'CLOSE_BRACKET': re.compile(r'\]'),
    'CONSTRUCTOR': re.compile(r'\.'),

    'LINE_SEP': re.compile(r';'),
    'CODEBLOCK': StatefulParser('{', '}'),

    'WHITESPACE': re.compile('\s+'),
}

def resolve(statement: str):
    if not statement or statement.isspace():
        return []

    tokens = []
    cache = ''
    matched = None
    statement = statement + ';'
    i = 0
    while i < len(statement):
        char = statement[i]
        matching = False
        if char != ';':
            for k, comp in TOKENIZATION_RULES.items():
                if comp.fullmatch(cache + char):
                    cache += char
                    matching = True
                    matched = k
                    break

            if matched is None:
                # Just assume that a match will appear, otherwise bad things happen; actually either way bad things would happen
                cache += char
                i += 1
                continue
                # raise errors.CompilerError('Cannot resolve character %s "%s" in "%s"' % (i, char, statement))

        if matched == 'WHITESPACE':
            continue

        if not matching:
            tokens.append((matched, cache.strip()))
            cache = ''
            matched = None
            if not char.isspace() and char != ';':
                continue
        i += 1

    print(tokens)
    return tokens