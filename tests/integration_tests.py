import datetime
import uuid
from unittest.mock import patch, Mock

from patch_target import patch_target
from tests import dummy_module


def test_patch_target_successfully_patches_object_using_unittestt_mock_patch_ctxt_mgr() -> None:
    with patch(patch_target(dummy_module, datetime)) as mock_dt:
        mock_dt.datetime.now.return_value = datetime.datetime(1970, 1, 1)

        actual = dummy_module.get_current_time()
        expected = datetime.datetime(1970, 1, 1)

        assert actual == expected


@patch(patch_target(dummy_module, uuid.uuid4))
def test_patch_decorator_with_patch_target(mock_uuid: Mock) -> None:
    new_id = uuid.uuid4()
    mock_uuid.return_value = new_id

    actual = dummy_module.generate_uuid()
    expected = new_id

    assert actual == expected


@patch(patch_target(dummy_module, "some_value"), {"foo": 123, "bar": 9892})
def test_patch_decorator_with_patch_target_for_module_attribute() -> None:
    actual = dummy_module.some_value
    expected = {"foo": 123, "bar": 9892}

    assert actual == expected
