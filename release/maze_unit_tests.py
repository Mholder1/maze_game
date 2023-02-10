import unittest
import maze_game_v2
import pathlib
from maze_game_v2 import game_t, LIST_CONFS
PATH = pathlib.PurePath(__file__).parent

#Tampered Configuration Files
L1_R1 = f"{PATH}/../tests/level_1/room_1"
L1_R2 = f"{PATH}/../tests/level_1/room_2"
L1_R3 = f"{PATH}/../tests/level_1/room_3"
L2_R1 = f"{PATH}/../tests/level_2/room_1"
L2_R2 = f"{PATH}/../tests/level_2/room_2"
L2_R3 = f"{PATH}/../tests/level_2/room_3"
L3_R1 = f"{PATH}/../tests/level_3/room_1"
L3_R2 = f"{PATH}/../tests/level_3/room_2"
L3_R3 = f"{PATH}/../tests/level_3/room_3"
TEST_LIST_CONFS = [L1_R1, L1_R2, L1_R3, L2_R1, L2_R2, L2_R3, L3_R1, L3_R2, L3_R3]

class TestStringMethods(unittest.TestCase):  
    def test_files_true(self):
        conf = game_t(1)
        valid = conf.check_configs_valid(LIST_CONFS)
        self.assertTrue(valid, True)
    
    def test_wrong_conf(self):
        wrong_conf = game_t(1)
        invalid = wrong_conf.check_configs_valid(TEST_LIST_CONFS)
        self.assertFalse(invalid, False)
    
if __name__ == '__main__':
    unittest.main()
