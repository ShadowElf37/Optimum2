from op_token import Token
from op_keywords import Let
import errors

class Equals(Token):
    def build(self):
        print('!!', self.context)
        for token in self.context_before():
            if token[0] == 'OPEN_PAR':
                return self.value  # If it's a kwarg etc.
        if self.last()[1] not in Let.ASSIGNED:
            raise errors.CompilerError('Variable assigned before it was created.')
        return self.value

class Add(Token):
    def build(self):
        return self.value

class Increment(Token):
    def build(self):
        return ' += 1'

class Subtract(Token):
    def build(self):
        return self.value

class Decrement(Token):
    def build(self):
        return ' -= 1'

class Multiply(Token):
    def build(self):
        return self.value

class Divide(Token):
    def build(self):
        return self.value

class Mod(Token):
    def build(self):
        return self.value

class CompareEquals(Token):
    def build(self):
        return self.value

class CompareGreater(Token):
    def build(self):
        return self.value

class CompareLess(Token):
    def build(self):
        return self.value

class CompareGreaterEqual(Token):
    def build(self):
        return self.value

class CompareLessEqual(Token):
    def build(self):
        return self.value

class Force(Token):
    def build(self):
        return '=0'
