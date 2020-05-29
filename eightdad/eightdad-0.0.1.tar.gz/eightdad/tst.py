
def build_registrar(d: dict):

    def registrar(pattern : int, first_nibbles):
        for first_nibble in first_nibbles:
            d[first_nibble] = pattern

    return registrar


a = {}
b = {}

a_f = build_registrar(a)
b_f = build_registrar(b)
print(a_f, b_f, a_f == b_f)