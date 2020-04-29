from op_token import Token
import re

class Int(Token):
    def build(self):
        return self.value

class Float(Token):
    def build(self):
        return self.value

class String(Token):
    def build(self):
        return '_String("' + self.value.strip("'").strip('"') + '")'


class CodeBlockRaw(Token):
    def build(self):
        self.code = self.value.strip('{').strip('}').strip().replace('::', ';')
        return '###'.join(self.compiler(self.code, scope='BLOCK'))
    def lines(self, indent=1):
        return ('\n'+'\t'*indent).join(self.build().split('###')).replace('$N$', '\n').replace('$T$', '\n')

class CodeBlock(Token):
    DEFINITIONS = []
    COUNTER = 0
    STRUCTURE =\
"""class {id}(__Optimum_Object_BASE):{static}
    def __new__(cls, {args}):{self}{constructor}
        {rval}"""
    def __init__(self, *args, argstr='', **kwargs):
        super().__init__(*args, **kwargs)
        self.id = '__Optimum_Object_%s' % self.COUNTER
        self.__class__.COUNTER += 1
        self.code = self.value.strip('{').strip('}').strip().replace('::', ';')
        self.argstr = argstr
        inst = self.host.find_behind('INAME', (self.host.find_next('CODEBLOCK') or 0)+1)
        if inst is not None:
            if self.argstr:
                self.argstr += (',' if self.argstr[-1] != ',' else '') + 'self,'
            else:
                self.argstr = 'self,'
            self.host.context[inst] = ('NAME', self.host.context[inst][1].strip('.'))

    def build(self):
        compiled = self.compiler(self.code, scope='BLOCK')
        rval = 'return self'
        func = False

        # FIND RETURN VALUE
        for i, line in enumerate(compiled):
            if re.fullmatch('^return .*$', line):
                compiled = compiled[:i]
                rval = line.strip()
                func = True
                break

        # BUILD CONSTRUCTOR
        compiled = '###'.join(compiled).replace('\n', '$N$').replace('\t', '$T$')

        remove = re.match('(<!--.*-->)', compiled)
        constructor = re.match('<!--(.*)-->', compiled)
        if remove is not None and constructor is not None:  # If it's defined by .
            remove = remove.groups()
            constructor = '\n\t\t'.join('\n'.join(constructor.groups()).replace('###', '\n\t\t').replace('$N$', '\n').replace('$T$', '\t').split('\n'))
            for group in remove:
                compiled = compiled.replace(group, '')
        elif func is True:  # If it's defined by a toplevel return
            constructor = '\n\t\t'.join('\n'.join(compiled.split('###')).replace('$N$', '\n').replace('$T$', '\t').split('\n'))
            compiled = ''

        compiled = compiled.split('###')


        # CREATE CLASS DEFINITION
        self.DEFINITIONS.append(self.STRUCTURE.format(
            id=self.id,
            static=('\n\t' + '\n\t'.join(compiled)) if any(compiled) else '',
            args=self.argstr,
            self='\n\t\tself = super().__new__(cls)' if not func else '',
            constructor=('\n\t\t' + constructor) if constructor else '',
            rval=rval
        ).replace('\t', '    '))

        return self.id
