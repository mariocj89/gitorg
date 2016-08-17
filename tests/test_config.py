import unittest
import mock
from gitorg import config


class TestConfig(unittest.TestCase):
    def test_empty_config_fails_to_retrieve_option(self):
        cfg = config.Config()
        self.assertRaises(KeyError, cfg["status"].__getitem__, "option")

    def test_config_with_element_is_returned(self):
        cfg = config.Config({"status": {"option": 1}})
        assert cfg["status"]["option"] == 1

    def test_config_global_config_loaded(self):
        cfg = config.Config({"global": {"option": 1}})
        assert cfg["status"]["option"] == 1

    def test_config_non_section_param(self):
        cfg = config.Config({"option": 5})
        assert cfg["option"] == 5

    def test_config_global_not_overrides(self):
        cfg = config.Config({"global": {"option": True}, "status": {"option": False}})
        assert cfg["status"]["option"] == False

    @mock.patch("gitorg.config.open", create=True)
    def test_save_config(self, open_mock):
        cfg = config.Config({"global": {"option": True}, "status": {"option": False}})
        cfg.save("filename")
        print open_mock.assert_called_with("filename", "w")

    @mock.patch("gitorg.config.open",
                mock.mock_open(read_data="""{"c":{"a":1}}"""),
                create=True)
    def test_load_config(self):
        cfg = config.Config.load("filename")
        assert cfg["c"]["a"] == 1


if __name__ == '__main__':
    unittest.main()
