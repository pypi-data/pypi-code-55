"""Functions for manipulating sequences."""
NT_TR = bytes.maketrans(b'gcatGCAT', b'cgtaCGTA')


def reverse_complement(seq: str) -> str:
    """Reverse complement sequence."""
    if isinstance(seq, memoryview):
        seq = bytes(seq)
    return seq[::-1].translate(NT_TR)
