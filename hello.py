width = 200
height = 100

print('P3\n%d %d\n255' % (width, height))

for y in range(height-1, -1, -1):
    for x in range(width):
        r = x / width   # 0 <= r < 1
        g = y / height  # 0 <= g < 1
        b = 0.2

        # Why multiply by 255.99 and not 255?
        ir = int(255.99 * r)
        ig = int(255.99 * g)
        ib = int(255.99 * b)

        print('%d %d %d' % (ir, ig, ib))
