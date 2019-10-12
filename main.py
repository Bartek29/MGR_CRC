from common.logger import Logger
from generator.parser import Parser

Logger.set_level(Logger.DEBUG)
Logger().info("Start")
p = Parser("schemas/k_capital_1.sch",
           move_point_rnd=2,
           paint_chance_rnd=0.8)
p.parse()
p.paint()

