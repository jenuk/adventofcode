def gcd_extended_rec(a: int, b: int) -> tuple[int, int, int]:
    # only included for readability
    # returns (d, k_a, k_b) with d = k_a * a + k_b * b
    if a < b:
        d, k_b, k_a = gcd_extended_rec(b, a)
        return d, k_a, k_b
    if b == 0:
        return a, 1, 0

    # a = q * b + r
    q, r = a // b, a % b
    d, k_b, k_r = gcd_extended_rec(b, r)
    # d = k_b * b + k_r * r
    # = k_b * b + k_r * (a - q*b)
    # = (k_b - k_r * q) * b + k_r * a
    return d, k_r, k_b - k_r * q


def gcd_extended(a: int, b: int) -> tuple[int, int, int]:
    # iterative, but less readable vesion of `gcd_extended_rec` above
    # returns (d, k_a, k_b) with d = k_a * a + k_b * b
    if a < b:
        d, k_b, k_a = gcd_extended(b, a)
        return d, k_a, k_b

    divs = []
    x, y = a, b
    while y != 0:
        divs.append(x // y)
        x, y = y, x % y

    d = x
    kx = 1
    ky = 0
    # we got d = kx * x + ky * y
    for q in divs[::-1]:
        # x = q*y + r
        kx, ky = ky, kx - ky * q
    return d, kx, ky


def gauss_sum(n: int) -> int:
    return (n * (n + 1)) // 2
