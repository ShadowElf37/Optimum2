import errors
import op_keywords, op_operators, op_names, op_literals, op_separators

CONSTRUCTORS = {
    'KEYWORD': {
        'let': op_keywords.Let,
        'is': op_keywords.Constant,
        'of': op_keywords.Temp,
        'return': op_keywords.Return,
        'true': op_keywords.true,
        'false': op_keywords.false,
        'null': op_keywords.Null,
        'for': op_keywords.For,
        'unpack': op_keywords.Unpack,
        'undefined': op_keywords.Undefined,
        'from': op_keywords.From,
        'while': op_keywords.While,
        'in': op_keywords.In,
        'if': op_keywords.If,
        'import': op_keywords.Import,
        'puts': op_keywords.Puts,
        'else': op_keywords.Else,
        'with': op_keywords.With,
        'try': op_keywords.Try,
        'catch': op_keywords.Catch,
    },

    'OP_EQ': op_operators.Equals,
    'OP_ADD': op_operators.Add,
    'OP_INC': op_operators.Increment,
    'OP_SUB': op_operators.Subtract,
    'OP_DEC': op_operators.Decrement,
    'OP_MUL': op_operators.Multiply,
    'OP_DIV': op_operators.Divide,
    'OP_MOD': op_operators.Mod,
    'OP_FORCE': op_operators.Force,
    'CMP_EQ': op_operators.CompareEquals,
    'CMP_GT': op_operators.CompareGreater,
    'CMP_LT': op_operators.CompareLess,
    'CMP_GE': op_operators.CompareGreaterEqual,
    'CMP_LE': op_operators.CompareLessEqual,

    'NAME': op_names.BareName,
    'INAME': op_names.InstanceName,
    'CONSTRUCTOR': op_names.Constructor,
    'CLASS': op_names.ClassRef,

    'INT': op_literals.Int,
    'FLOAT': op_literals.Float,
    'STRING': op_literals.String,

    'OPEN_PAR': op_separators.Parenthesis,
    'CLOSE_PAR': op_separators.Parenthesis,
    'OPEN_BRACKET': op_separators.OpenBracket,
    'CLOSE_BRACKET': op_separators.CloseBracket,
    'COMMA': op_separators.Comma,

    'LINE_SEP': op_separators.LineSep,
    'CODEBLOCK': op_literals.CodeBlock,
}


def verify(value, token):
    if value is None:
        raise errors.CompilerError('Unrecognized token "%s" (%s)' % (value, token))

def construct(token, index, context, compiler, host=None, force=None, force_args=(), force_kwargs=dict(), scope='GLOBAL'):
    c = force
    if c is None:
        c = CONSTRUCTORS.get(token[0])
        verify(c, token)
        if type(c) is dict:
            c = c.get(token[1])
            verify(c, token)

    return c(index, context, construct, build, token, compiler, host=host, scope=scope, *force_args, **force_kwargs)

def build(tokens, compiler, host=None, scope='GLOBAL'):
    # host is any parent Token class so a child can hook onto the build process and add aftereffects
    for i, token in enumerate(tokens):
        if token[0] in ['KEYWORD', 'CONSTRUCTOR']:
            return construct(token, i, tokens, compiler, host=host, scope=scope).build()

    #for i, token in enumerate(tokens):
    #    if 'CMP' in token[0] or 'OP' in token[0]:
    #        return construct(token, i, tokens, compiler, host=host).build()

    cnsts = []
    for i, token in enumerate(tokens):
        cnsts.append(construct(token, i, tokens, compiler, host=host, scope=scope).build())
    return ''.join(cnsts)
