class AttachPrePost(type):
    def __new__(meta, name, mro, d):
        cls = type.__new__(meta, name, mro, dict(d))
        old_build = cls.build
        def new_build(self, *args, **kwargs):
            built = old_build(self, *args, **kwargs)
            return ''.join(self.pre) + built + ''.join(self.post)
        cls.build = new_build
        return cls


class Token(metaclass=AttachPrePost):
    END = object()
    def __init__(self, pos, statement, constructor, builder, token, compiler, host=None, scope='GLOBAL'):
        self.position = pos
        self.context = statement
        self.constructor = constructor  # Generates Token-like class
        self._builder = builder  # Constructs and builds from an unconstructed token tree
        self.key = token[0]
        self.value = token[1]
        self.compiler = compiler
        self.host = host or self
        self.scope = scope
        self.pre = []
        self.post = []

    def builder(self, tokens, host=None):
        return self._builder(tokens, self.compiler, host or self)

    def delta(self, i):
        try:
            return self.context[self.position + i]
        except IndexError:
            return None

    def context_after(self, i=0):
        return self.context[self.position + i + 1:]
    def context_before(self, i=0):
        print(self.position + i)
        return self.context[:self.position + i]

    def construct_delta(self, i):
        return self.constructor(self.delta(i), self.position + i, self.context, self.compiler, host=self)

    def build_deltas(self, *indices):
        #if self.END == indices[-1]:
        #    indices = indices[:-1] + tuple(max(indices[:-1]) + i + 1 for i in range(0, len(self.context)-max(indices[:-1]) - 1))
        return ''.join(self.construct_delta(i).build() for i in indices)

    def build_out(self, from_i=1, to=-1, *args, **kwargs):
        if to != -1:
            return self.builder(self.context_after(0)[from_i-1: to], *args, **kwargs)
        return self.builder(self.context_after(0)[from_i-1: len(self.context_after(from_i-1))+1], *args, **kwargs)

    def next(self):
        return self.delta(1)
    def last(self):
        return self.delta(-1)

    def find_next(self, token_name, from_i=0):
        for i, token in enumerate(self.context_after(from_i)):
            if token[0] == token_name:
                return i
        return None
    def find_behind(self, token_name, from_i=0):
        for i, token in enumerate(self.context_before(from_i)):
            if token[0] == token_name:
                return i
        return None
    def find_last(self, token_name, from_i=0):
        f = None
        for i, token in enumerate(self.context_after(from_i)):
            if token[0] == token_name:
                f = i
        return f

    def build_delta_as(self, index, type, *args, build=True, **kwargs):
        const = self.constructor(self.delta(index), self.position + index, self.context, self.compiler, host=self, force=type, force_args=args, force_kwargs=kwargs)
        return const.build() if build else const

    def register_pre(self, effect):
        self.host.pre.append(effect)
    def register_post(self, effect):
        self.host.post.append(effect)

    def build(self):
        pass
