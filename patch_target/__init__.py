import typing
from types import ModuleType
from typing import Protocol, NewType, Any, TypeGuard, Callable

PatchTarget = NewType("PatchTarget", str)
NamedCallable: typing.TypeAlias = Callable[[Any], Any]


@typing.runtime_checkable
class Named(Protocol):
    __name__: str


UnverifiedVisitorCandidate = Any
VisitorCandidate = NewType("VisitorCandidate", str)
ModulePathElement = str


class InvalidPatchTargetException(Exception):
    pass


class UnpatchableModuleAttributeTypeError(Exception):
    pass



def get_visitor_candidates_from_path_element_list(
    module_path_elements: list[ModulePathElement],
) -> typing.Generator[VisitorCandidate, None, None]:
    return (
        VisitorCandidate(".".join(module_path_elements[i:]))
        for i in range(len(module_path_elements))
    )


def get_verified_visitor_candidates(
    candidate: UnverifiedVisitorCandidate,
) -> typing.Generator[VisitorCandidate, UnpatchableModuleAttributeTypeError, None]:
    match candidate:
        case str():
            for c in [VisitorCandidate(candidate)]:
                yield c
        case Named():
            for c in get_visitor_candidates_from_path_element_list(
                candidate.__name__.split(".")
            ):
                yield c
        case _:
            raise UnpatchableModuleAttributeTypeError(
                "object_to_be_patched does not have a __name__ attribute. You may need to pass the name as a string."
            )


def patch_target(
    host_module: ModuleType, object_to_be_patched: UnverifiedVisitorCandidate
) -> PatchTarget:
    for visitor_candidate in get_verified_visitor_candidates(object_to_be_patched):
        if hasattr(host_module, visitor_candidate):
            return PatchTarget(f"{host_module.__name__}.{visitor_candidate}")

    name_of_visitor = getattr(object_to_be_patched, "__name__", object_to_be_patched)

    raise InvalidPatchTargetException(
        f"'{name_of_visitor}' not found within {host_module.__name__}"
    )


__all__ = ["patch_target"]
