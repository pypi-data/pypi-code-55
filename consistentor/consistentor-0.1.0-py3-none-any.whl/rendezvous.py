import xxhash


def rendezvous_hash(key, items):
    selected = None
    highest_score = -1
    for item in items:
        score = xxhash.xxh64_intdigest(f"{key}{item}")
        if score > highest_score:
            selected = item
            highest_score = score
    return selected
