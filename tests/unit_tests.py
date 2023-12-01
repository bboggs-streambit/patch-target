import datetime
import uuid
from uuid import uuid4

import pytest  # type: ignore

from patch_target import (
    patch_target,
    InvalidPatchTargetException,
    PatchTarget,
    get_visitor_candidates_from_path_element_list,
    get_verified_visitor_candidates,
    UnpatchableModuleAttributeTypeError,
)
from tests import dummy_module, dummy_other_module
from tests.dummy_module import some_value
from tests.dummy_other_module.nested_dummy_other_module import (
    more_nesting_of_the_dummy_other_module,
)


def test_patch_target_returns_string_concatenation_of_full_path_within_module_to_target() -> None:
    actual_str_path = patch_target(dummy_module, datetime)
    expected_str_path = PatchTarget("tests.dummy_module.datetime")
    assert actual_str_path == expected_str_path


def test_patch_target_raises_invalid_patch_target_exc_if_object_to_be_patched_not_in_module() -> None:
    with pytest.raises(InvalidPatchTargetException) as e:
        patch_target(dummy_module, uuid)

    assert str(e.value) == "'uuid' not found within tests.dummy_module"


def test_patch_target_raises_object_missing_name_attribute_exception_if_object_to_be_patched_lacks_name_attribute() -> None:
    with pytest.raises(InvalidPatchTargetException) as e:
        patch_target(dummy_module, "chickens")

    assert str(e.value) == "'chickens' not found within tests.dummy_module"


def test_patch_target_returns_string_concatenation_of_full_path_to_function_to_target() -> None:
    actual_str_path = patch_target(dummy_module, uuid4)
    expected_str_path = PatchTarget("tests.dummy_module.uuid4")

    assert actual_str_path == expected_str_path


def test_patch_target_overrides_module_level_variables() -> None:
    actual_str_path = patch_target(dummy_module, "some_value")
    expected_str_path = PatchTarget("tests.dummy_module.some_value")

    assert actual_str_path == expected_str_path


def test_patch_target_overrides_module_level_variables_raises_unpatchable_module_attribute_type_error() -> None:
    with pytest.raises(UnpatchableModuleAttributeTypeError) as e:
        patch_target(dummy_module, some_value)

    assert e.type is UnpatchableModuleAttributeTypeError


def test_patch_target_overrides_module_level_variables_raises_unpatchable_module_attribute_type_error_with_helpul_error_message() -> None:
    with pytest.raises(UnpatchableModuleAttributeTypeError) as e:
        patch_target(dummy_module, some_value)

    assert (
        str(e.value)
        == "object_to_be_patched does not have a __name__ attribute. You may need to pass the name as a string."
    )


def test_patch_target_provides_valid_patch_string_for_local_module() -> None:
    actual_str_path = patch_target(dummy_module, dummy_other_module)
    expected_str_path = PatchTarget("tests.dummy_module.dummy_other_module")

    assert actual_str_path == expected_str_path


def test_get_visitor_candidates_from_path_element_list() -> None:
    module_path_elements = ["path", "to", "my", "cool", "submodule", "yay"]
    expected_visitor_candidates = [
        "path.to.my.cool.submodule.yay",
        "to.my.cool.submodule.yay",
        "my.cool.submodule.yay",
        "cool.submodule.yay",
        "submodule.yay",
        "yay",
    ]

    actual = list(get_visitor_candidates_from_path_element_list(module_path_elements))

    assert actual == expected_visitor_candidates


def test_process_unverified_candidate_with_module_type() -> None:
    visiting_module = more_nesting_of_the_dummy_other_module
    expected = [
        "tests.dummy_other_module.nested_dummy_other_module.more_nesting_of_the_dummy_other_module",
        "dummy_other_module.nested_dummy_other_module.more_nesting_of_the_dummy_other_module",
        "nested_dummy_other_module.more_nesting_of_the_dummy_other_module",
        "more_nesting_of_the_dummy_other_module",
    ]
    actual = list(get_verified_visitor_candidates(visiting_module))

    assert actual == expected


def test_process_unverified_candidate_with_string_type():
    visiting = "attribute"
    actual = list(get_verified_visitor_candidates(visiting))
    expected = [visiting]

    assert actual == expected


def test_proces_unverified_candidate_with_function_type():
    visiting = uuid4
    actual = list(get_verified_visitor_candidates(visiting))
    expected = ["uuid4"]

    assert actual == expected
