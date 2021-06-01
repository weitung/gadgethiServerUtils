import unittest
import copy
from gadgethiServerUtils._configs import *
from gadgethiServerUtils._exceptions import *

class PrimitiveTests(unittest.TestCase):
    """
    Testing Strategy:
    - GServerConfigs
        * constructor
            - partition on flags: doday_flag, aws_flag, no_flag
        * check_req
            - partition on input dict: empty dictionary, >0 keys dictionary
            - partition on return: fully matched, one matches, fully no match
    """

    # covers configs modes
    def test_configs_generation(self):
        gconfigs = GServerConfigs()
        self.assertTrue(set(gconfigs.basic_configs.keys()).issubset(set(gconfigs.__dict__.keys())), \
            "Check basic configs generation")

        gconfigs = GServerConfigs(aws_flag=True)
        test_configs = {}
        test_configs.update(GServerConfigs.basic_configs)
        test_configs.update(GServerConfigs.aws_configs)
        self.assertTrue(set(test_configs.keys()).issubset(set(gconfigs.__dict__.keys())), \
            "Check aws configs generation")

        gconfigs = GServerConfigs(doday_flag=True)
        test_configs = {}
        test_configs.update(GServerConfigs.basic_configs)
        test_configs.update(GServerConfigs.doday_configs)
        self.assertTrue(set(test_configs.keys()).issubset(set(gconfigs.__dict__.keys())), \
            "Check doday configs generation")

    # covers check req
    def test_check_configs_requirements_matching(self):
        status, modified_dict = GServerConfigs.check_current_configs_match_reqs({})
        self.assertFalse(status)
        self.assertEqual(modified_dict, GServerConfigs.basic_configs)


        status, modified_dict = GServerConfigs.check_current_configs_match_reqs(GServerConfigs.basic_configs)
        self.assertTrue(status)
        self.assertEqual(modified_dict, GServerConfigs.basic_configs)

        test_configs = {
            "log_file_path": "dummy_path",
            "some_random_key": "some_random_value"
        }
        status, modified_dict = GServerConfigs.check_current_configs_match_reqs(test_configs)
        result_configs = copy.deepcopy(GServerConfigs.basic_configs)
        result_configs.update(test_configs)
        self.assertFalse(status)
        self.assertEqual(modified_dict, result_configs)


