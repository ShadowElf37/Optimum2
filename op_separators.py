from op_token import Token

class Comma(Token):
    def build(self):
        return self.value

class OpenBracket(Token):
    def build(self):
        return '_Array(' + self.value

class CloseBracket(Token):
    def build(self):
        return self.value + ')'

class Parenthesis(Token):
    def build(self):
        return self.value

class LineSep(Token):
    def build(self):
        return '\n'
