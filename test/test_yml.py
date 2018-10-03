import pytest

from pyduino.models import SetupConfig, Board


@pytest.fixture
def cfg():
    return SetupConfig('test/resources/good_setup.yml')


def test_config_raise_value_error_on_wrong_path():
    with pytest.raises(ValueError):
        SetupConfig('non/existing/path.yml')


def test_config_has_boards_attr(cfg):
    assert hasattr(cfg, 'boards')


def test_config_has_two_boards(cfg):
    assert len(cfg.boards) == 2


def test_config_boards_type(cfg):
    board_0 = cfg.boards[0]
    board_1 = cfg.boards[1]

    assert type(board_0) is Board
    assert type(board_1) is Board


def test_board_0_has_id_0(cfg):
    board_id = cfg.boards[0].id

    assert board_id == 0


def test_board_0_has_2_sensors(cfg):
    sensors = cfg.boards[0].sensors

    assert len(sensors) == 2


def test_board_0_has_1_relay(cfg):
    relays = cfg.boards[0].relays

    assert len(relays) == 1


def test_board_1_has_id_1(cfg):
    board_id = cfg.boards[1].id

    assert board_id == 1

def test_board_1_has_1_sensor(cfg):
    sensors = cfg.boards[1].sensors

    assert len(sensors) == 1


def test_board_1_has_no_relays(cfg):
    relays = cfg.boards[1].relays

    assert len(relays) == 0


def test_sensor_uimidity00_has_right_id(cfg):
    board = cfg.boards[0]
    sensor_id = board.sensors['uimidity00'].id

    assert sensor_id == 'uimidity00'


def test_sensor_uimidity00_is_type_humidity(cfg):
    board = cfg.boards[0]
    sensor_type = board.sensors['uimidity00'].type

    assert sensor_type == 'humidity'


def test_sensor_uimidity00_has_digital_port_type(cfg):
    board = cfg.boards[0]
    sensor_port_type = board.sensors['uimidity00'].port_type

    assert sensor_port_type == 'D'


def test_sensor_uimidity00_has_port_code_12(cfg):
    board = cfg.boards[0]
    sensor_port_type = board.sensors['uimidity00'].port_code

    assert sensor_port_type == 12

def test_relay_relay00_has_right_id(cfg):
    board = cfg.boards[0]
    relay_id = board.relays['relay00'].id

    assert relay_id == 'relay00'


def test_relay_relay00_is_type_relay(cfg):
    board = cfg.boards[0]
    relay_type = board.relays['relay00'].type

    assert relay_type == 'relay'


def test_relay_relay00_has_digital_port_type(cfg):
    board = cfg.boards[0]
    relay_port_type = board.relays['relay00'].port_type

    assert relay_port_type == 'D'


def test_relay_relay00_has_port_code_53(cfg):
    board = cfg.boards[0]
    relay_port_type = board.relays['relay00'].port_code

    assert relay_port_type == 53


def test_relay_relay00_is_on_equals_true(cfg):
    board = cfg.boards[0]
    relay_is_on = board.relays['relay00'].is_on

    assert relay_is_on == 'on'


def test_sensor_huimidity00_has_analog_port_type(cfg):
    board = cfg.boards[1]
    relay_port_type = board.sensors['huimidity00'].port_type

    assert relay_port_type == 'A'


def test_wrong_relay_default_status_raises_error():
    with pytest.raises(ValueError):
        SetupConfig(
            'test/resources/wrong_relay_default_status.yml'
        )


def test_wrong_port_type_raises_error():
    with pytest.raises(ValueError):
        SetupConfig(
            'test/resources/wrong_port_type.yml'
        )


def test_wrong_port_code_type_raises_error():
    with pytest.raises(ValueError):
        SetupConfig(
            'test/resources/wrong_port_code_type.yml'
        )

def test_no_port_code_raises_error():
    with pytest.raises(ValueError):
        SetupConfig(
            'test/resources/no_port_code.yml'
        )
