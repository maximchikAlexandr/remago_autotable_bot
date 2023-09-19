import string


VALID_LITTERS = "ABEKMHOPCTX"
INVALID_LITTERS = "АВЕКМНОРСТХ"


def to_format_sign(sign: str) -> str:
    dct = {ord(l): ord(VALID_LITTERS[ind]) for ind, l in enumerate(INVALID_LITTERS)}
    dct.update({ord(l): None for l in string.whitespace})
    dct.update({ord("-"): None})
    sign = sign.upper()
    sign = sign.translate(dct)
    return sign
