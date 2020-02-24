import os
from PIL import Image

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk('database/real_test/'):
    for file in f:
        files.append(os.path.join(r, file))

for index, f in enumerate(files):
    if index % 1000 == 0:
        print("{}/{} {}% | {}".format(index, len(files), index / len(files) * 100.0, f))
    img = Image.open(f)
    pixel_map = img.load()
    min_y = 127
    max_y = 0
    min_x = 127
    max_x = 0
    for y in range(img.size[0]):
        for x in range(img.size[1]):
            if pixel_map[x, y] == (0, 0, 0):
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
    min_y = min_y - 1 if min_y > 1 else min_y
    min_x = min_x - 1 if min_x > 1 else min_x
    max_y = max_y + 1 if max_y < 126 else max_y
    max_x = max_x + 1 if max_x < 126 else max_x

    region = img.crop((min_x, min_y, max_x, max_y))
    region.thumbnail((32, 32))
    region = region.convert('L')
    new = Image.new(img.mode, (32, 32), (255, 255, 255))
    new.paste(region)
    new.save(f)
