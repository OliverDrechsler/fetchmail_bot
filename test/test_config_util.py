import pytest
import sys
import os

from unittest.mock import patch, mock_open
from config.config_util import Configuration, YamlReadError

import unittest

# set module path for testing
sys.path.insert(0, "test")

class TestConfiguration:
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="telegram:\n  token: '123456'\n  chat_number: ['1']\n  additional_list: ['user1']\n  allow_list: [{'user': 'id'}]",
    )
    @patch("os.path.isfile", return_value=True)
    def test_read_valid_config_file(self, mock_isfile, mock_file):
        """Test that Configuration correctly reads and parses a valid YAML configuration file."""
        config = Configuration()
        assert config.telegram_token == "123456"
        assert config.telegram_chat_nr == ["1"]
        assert config.additional_list == ["user1"]
        assert config.user_dict == {"user": "id"}

    @patch("os.path.isfile", side_effect=FileNotFoundError)
    def test_read_config_file_not_found(self, mock_isfile):
        with pytest.raises(FileNotFoundError):
            Configuration()

    @patch("builtins.open", new_callable=mock_open, read_data=": invalid\nyaml: file")
    @patch("os.path.isfile", return_value=True)
    def test_read_config_invalid_yaml_file(self, mock_isfile, mock_open):
        with pytest.raises(YamlReadError):
            Configuration()
