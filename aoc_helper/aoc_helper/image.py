def save_bitmap(grid: list[list[bool]], filename: str):
    n, m = len(grid), len(grid[0])

    data = bytearray(b"")
    for row in grid:
        byte = 0
        bit_count = 0
        for x in row:
            byte = (byte << 1) + bool(x)
            bit_count += 1

            if bit_count == 8:
                data.append(byte)
                bit_count = 0
                byte = 0
        if bit_count > 0:
            data.append(byte << (8 - bit_count))

    with open(filename, "wb") as file:
        file.write(f"P4\n{m} {n}\n".encode())
        file.write(data)
