import re
import math

class _String(str):
    def match(self, regex):
        return re.match(regex, self).groups()

class _Array(list):
    @property
    def length(self):
        return len(self)
    def push(self, item):
        self.append(item)

class _UNDEFINED_CLASS:
    def __repr__(self):
        return 'undefined'
    def __str__(self):
        return None
    def __eq__(self, other):
        return False

__UNDEFINED = _UNDEFINED_CLASS()

class __Optimum_Object_BASE:
    def __getitem__(self, item):
        return getattr(self, item, None)
    def __setitem__(self, item):
        return setattr(self, item, None)