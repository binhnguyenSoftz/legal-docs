import hashlib
import random


def derive_seed(master_seed: int, *parts: object) -> int:
    """Seed ổn định cho từng hồ sơ/giấy tờ, không phụ thuộc thứ tự sinh hay PYTHONHASHSEED."""
    key = ":".join(str(p) for p in (master_seed, *parts)).encode()
    return int.from_bytes(hashlib.sha256(key).digest()[:8], "big")


def weighted_choice(rng: random.Random, items: list, weights: list[float]):
    return rng.choices(items, weights=weights, k=1)[0]
