from setuptools_gitver import get_version

from ._dictable import Dictable
from ._fields import PolyField, PolyListField
from ._list import ObjectList
from ._utils import update_module_attributes

__version__ = get_version(__name__)

__all__ = [
    'Dictable',
    'ObjectList',
    'PolyField',
    'PolyListField',
]

update_module_attributes(__name__, __all__)
