import unittest

from common.logger import Logger

from generator.ut.ut_parser import TestLine
from generator.ut.ut_parser import TestPoint

if __name__ == "__main__":
    Logger.set_level(Logger.NONE)
    unittest.main()
