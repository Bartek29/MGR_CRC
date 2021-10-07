from common.logger import Logger
from generator.parser import Parser
from PIL import Image

Logger.set_level(Logger.INFO)

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
         'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
for c in chars:
    for i in range(2000):
        Logger().error("Create {}: {}/2000".format(c, i))
        p = Parser("schemas/{}_capital_1.sch".format(c),
                   move_point_rnd=2,
                   paint_chance_rnd=0.8)
        p.parse()
        p.paint()
        img = Image.open('test.bmp')

        new_img = img.resize((32, 32))
        new_img.save('database/gen_train/{}_capital/train_{:04d}.png'.format(c, i), 'png')
