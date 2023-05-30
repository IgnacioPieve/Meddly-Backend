from datetime import datetime


def ranges_intersect(a, b, c, d):
    if medicine_start <= end and start <= medicine_end:
        return True
    return False

medicine_start = datetime(2023, 1, 5)
medicine_end = datetime(2023, 1, 10)
start = datetime(2023, 1, 4)
end = datetime(2023, 1, 6)

intersect = ranges_intersect(medicine_start, medicine_end, start, end)
print(intersect)