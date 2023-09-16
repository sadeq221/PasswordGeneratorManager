import pytest
from project import open_setting, Master_password_reuirements, main_page
from unittest.mock import patch


# Test Master_password_reuirements function
def test_Master_password_reuirements():

    with pytest.raises(ValueError):

        # Check password with invalid length
        Master_password_reuirements(".Ad5252")

        # Test password without number
        Master_password_reuirements(".Adadadad")

        # Test password without symbol
        Master_password_reuirements("Adad5252")

        # Test password without Upper
        Master_password_reuirements(".adad5252")

        # Test password without lower
        Master_password_reuirements(".ADAD5252")


# Test open_setting function
@patch('project.input')
@patch('project.main_page')
@patch('project.set_master_password')
def test_open_setting(mock_set_master_password, mock_main_page, mock_input):

    mock_set_master_password.return_value = "set master password function called"
    mock_main_page.return_value = "main page function called"

    # Test b input
    mock_input.return_value = "b"
    assert open_setting() == "main page function called"

    # Test m input
    mock_input.return_value = "m"
    assert open_setting() == "set master password function called"

    # Test two wrong inputs followed by 'b'
    mock_input.side_effect = "wrong", "nope", "b"
    assert open_setting() is "main page function called"


# Test open_setting function
@patch('project.input')
@patch('project.open_setting')
@patch('project.set_new_account_name')
def test_main_page(mock_set_new_account_name, mock_open_setting, mock_input):

    mock_set_new_account_name.return_value = "set_new_account_name function called"
    mock_open_setting.return_value = "open_setting function called"

    # Test e input
    with pytest.raises(SystemExit):
        mock_input.return_value = "e"
        main_page()

    # Test s input
    mock_input.return_value = "s"
    assert main_page() == "open_setting function called"

    # Test a input
    mock_input.return_value = "a"
    assert main_page() == "set_new_account_name function called"

    # Test two wrong inputs followed by 'b'
    mock_input.side_effect = "wrong", "nope", "s"
    assert main_page() == "open_setting function called"
