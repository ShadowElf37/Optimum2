from op_token import Token
from op_literals import CodeBlockRaw

class BareName(Token):
    def build(self):
        return self.value

class InstanceName(Token):
    def build(self):
        if self.last()[0] not in ['KEYWORD']:
            return self.value
        return 'self' + self.value

class Constructor(Token):
    def build(self):
        if self.find_next('CODEBLOCK') is None:
            return 'self'
        return '<!--' + self.build_delta_as(1, CodeBlockRaw) + '-->'

class ClassRef(Token):
    def build(self):
        return 'self.__class__'

