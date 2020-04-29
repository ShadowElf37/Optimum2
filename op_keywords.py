from op_token import Token
from op_literals import CodeBlock, CodeBlockRaw
import errors

class Let(Token):
    ASSIGNED = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def build(self):
        _next = self.context_after(0)
        if self.delta(2) is None:
            name = self.build_deltas(1)
            self.__class__.ASSIGNED.append(name)
            return name + '=__UNDEFINED'

        if _next[1][0] == 'CODEBLOCK':
            if self.scope == 'BLOCK':
                value = self.build_out(2)
                name = self.build_deltas(1)
                self.__class__.ASSIGNED.append(name)
                return name + ' = ' + value  # Render the name after the class is built in case it overrides the name, like to scrub self.x etc.
            name = self.build_deltas(1)
            self.__class__.ASSIGNED.append(name)
            CodeBlock.DEFINITIONS.append(name + ' = ' + self.build_out(2) + '\n')
            return '# Class definition was here'

        name = self.build_deltas(1)
        self.__class__.ASSIGNED.append(name)

        i = 1
        while _next[i][0] not in ['OP_EQ', 'OP_FORCE']:
            i += 1
        return self.build_out(i)

class Constant(Token):
    def build(self):
        return self.build_deltas(-1) + ' = ' + self.builder(self.context_after(0))

class Temp(Token):
    def build(self):
        name = self.build_deltas(-1)
        value = self.build_out(host=self.host)
        self.register_pre(name + ' = ' + value + '\n')
        self.register_post('\ndel ' + name)
        return name

class Return(Token):
    def build(self):
        return 'return ' + self.build_out()

class Unpack(Token):
    def build(self):
        return '__dict__.update(' + self.build_deltas(1) + '.__dict__)'

class true(Token):
    def build(self):
        return 'True'

class false(Token):
    def build(self):
        return 'False'

class Null(Token):
    def build(self):
        return 'None'

class Undefined(Token):
    def build(self):
        return '__UNDEFINED'

class For(Token):
    def build(self):
        ex = self.find_last('CODEBLOCK')
        if ex is None:
            raise errors.CompilerError
        return 'for i,' + self.build_deltas(1, 2) + 'enumerate(' + self.build_out(3, to=ex) + '):\n\t' + self.build_delta_as(ex + 1, CodeBlockRaw, build=False).lines()

class In(Token):
    def build(self):
        return ' in '

class While(Token):
    def build(self):
        ex = self.find_last('CODEBLOCK')
        if ex is None:
            raise errors.CompilerError
        return 'while ' + self.build_out(to=ex) + ':\n\t' + '\n\t'.join(self.build_delta_as(ex+1, CodeBlockRaw).split('###'))

class From(Token):
    def build(self):
        return self.build_delta_as(-1, CodeBlock, argstr=self.build_out())

class Import(Token):
    def build(self):
        return 'import ' + self.build_out()

class If(Token):
    def build(self):
        ex = self.find_last('CODEBLOCK')
        return 'if (' + self.build_out(to=ex) + '):\n\t' + self.build_delta_as(ex+1, CodeBlockRaw, build=False).lines()

class Else(Token):
    def build(self):
        if self.next()[1] == 'if':
            return 'el' + self.builder(self.context_after())
        return 'else:\n\t' + self.build_delta_as(1, CodeBlockRaw, build=False).lines()

class Try(Token):
    def build(self):
        ex = self.find_last('CODEBLOCK')
        return 'try:\n\t' + self.build_delta_as(ex+1, CodeBlockRaw, build=False).lines()

class Catch(Token):
    def build(self):
        ex = self.find_last('CODEBLOCK')
        return 'except:\n\t' + self.build_delta_as(ex+1, CodeBlockRaw, build=False).lines()

class With(Token):
    def build(self):
        ex = self.find_last('CODEBLOCK')
        name = self.build_deltas(1)
        Let.ASSIGNED.append(name)
        block = self.build_delta_as(ex+1, CodeBlockRaw, build=False)
        temp = self.build_out(to=ex, host=block)
        return block.build()

class Puts(Token):
    def build(self):
        return 'print(' + self.build_out() + ')'
