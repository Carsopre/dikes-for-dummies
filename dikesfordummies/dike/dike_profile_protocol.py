from typing import List, Protocol

from shapely.geometry import Point
from typing_extensions import runtime_checkable


@runtime_checkable
class DikeProfileProtocol(Protocol):
    characteristic_points: List[Point]
    height: float
    width: float
