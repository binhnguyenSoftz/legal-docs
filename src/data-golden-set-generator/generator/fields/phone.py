import random

# Đầu số di động 10 số hiện hành.
MOBILE_PREFIXES = [
    "032", "033", "034", "035", "036", "037", "038", "039", "086", "096", "097", "098",  # Viettel
    "070", "076", "077", "078", "079", "089", "090", "093",                              # MobiFone
    "081", "082", "083", "084", "085", "088", "091", "094",                              # VinaPhone
    "052", "056", "058", "092",                                                          # Vietnamobile
]


def generate(rng: random.Random) -> str:
    return rng.choice(MOBILE_PREFIXES) + f"{rng.randrange(10**7):07d}"


def validate(number: str) -> list[str]:
    if len(number) != 10 or not number.isdigit():
        return ["Không đủ 10 chữ số"]
    if number[:3] not in MOBILE_PREFIXES:
        return ["Đầu số không hợp lệ"]
    return []
