from cs50 import get_int


while True:
    height = get_int("Height:")
    if height < 9 and height > 0:
        break
for i in range(height):
    line = (" " * ((height-i)-1) + ("#" * (i+1)))
    print(line)