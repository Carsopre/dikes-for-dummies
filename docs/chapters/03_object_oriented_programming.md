# Chapter 03. Objected Oriented Programming in Python

Catching up? Just run the following command in your command line:
```
conda env create -f environment.yml
conda activate dikes-for-dummies_env
poetry install
```

You can follow the contents of this chapter now :)

## Intro
We have already seen the perks and pitfalls of Python as a dynamic language and its `duck typing`. Now we will explore both object oriented _foundations_ and _solid_ concepts applied through Python programming.

## Foundations
* [Encapsulation](#encapsulation).
    * Define public, protected and private data.
    * Public data can be accessed ‘from the outside’.
    * Protected data only internally (when using inheritance).
    * Private data only in the declared class.
* [Inheritance](#inheritance) and [abstractions](#abstractions):
    * Definition of generic functionality and properties in the base class.
    * Concrete methods in the inherited classes.
    * Abstract classes need a concrete inherited class (specialisation).
    * A class can inherit from an abstract class or another concrete class.
* [Polymorphism](#polymorphism).
    * The same interface applies for different data types or classes
    * Can be applied to classes (through inheritance) and methods.
* Aggregation and composition.
    * **Aggregation**: the associated objects do not need each other ‘to exist’.
    * **Composition**: the associated objects ‘need’ each other to ‘coexist’. The main object owns

### Encapsulation
In python encapsulation does not really exist, think of it more like a 'rule of conduct'. We identify protected (internal) methods and  parameters with a simple underscore `_` and private with double `__` so:
* `def _get_my_variable(...) -> Any` is meant to be used only while developing in the tool. Preferrebly within an instanced object.
* `def __get_my_variable(...) -> Any` is only meant to be used within its class / module. And not to be exposed.

```python
class BasicEncapsulation:
    def __init__(self):
        self.public_property = 42
        self._protected_property = 4.2
        self.__private_property = 0.42

    def public_method(self):
        pass

    def _protected_method(self):
        pass

    def __private_method(self):
        pass
```

### Inheritance
We have already shown simple inheritance, but of course Python allows us to do multiple inheritance whenever needed.

```python
class DikeProfile:

    characteristic_points: List[Point]

    def __init__(self) -> None:
        self.characteristic_points = []

class DikeReinforcement:
    reinforcement_input: DikeReinforcementInput

    def __init__(self) -> None:
        self.reinforcement_input = None

class DikeReinforcementProfile(DikeProfile, DikeReinforcement):
    def __str__(self) -> str:
        return "Reinforced Profile"


_drp = DikeReinforcementProfile()
assert isinstance(_drp, DikeReinforcement)
assert isinstance(_drp, DikeProfile)
assert isinstance(_drp, DikeReinforcement)
```

### Abstractions
To create abstract methods or classes we use the library `ABC`:

```python
from abc import ABC, abstractmethod

class DikeProfileBase(ABC):
    characteristic_points: List[Point]

    def __init__(self) -> None:
        self.characteristic_points = []

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError("Implement in concrete class")

    def set_points_from_tuples(self, tuple_list: List[Tuple[float, float]]):
        if not tuple_list:
            raise ValueError("tuple_list argument required.")
        self.characteristic_points = list(map(Point, tuple_list))

class DikeProfile(DikeProfileBase):
    ...
    def __str__(self) -> str:
        return "Initial Dike Profile"
    
    @classmethod
    def from_tuple_list(cls, tuple_list: List[Tuple[float, float]]) -> DikeProfile:
        _dike = cls()
        _dike.set_points_from_tuples(tuple_list)
        return _dike

assert issubclass(DikeProfile, DikeProfileBase)
```

### Polymorphism

Although it's possible to apply polymorphism in Python. In my experience is seldom used. Concrete methods and well-applied [SRP](#single-responsibility-principle) provide better code.

```python
class DikeProfileCalculator:
    def calculate_characteristic_points(self):
        # Base dike profile operations.
        pass
class PipingDikeProfileCalculator(DikeProfileCalculator):
    def calculate_characteristic_points(self):
        # Reinforcement piping dike operations.
        return super().calculate_characteristic_point
```

## SOLID

### Single responsibility principle.
By creating 'builders' and leaving the classes only as datastructures we reduce the amount of responsibility a class needs to do.


### Open for extension, closed for modification.
A class should be extendable without modifying the class itself. Whenever you start having an `if-else` to differenciate behaviors, try to create a new concrete class.

* Given:
```python
class DikeMaterial:
    def __init__(self, cost: float, material_type: str):
        self.cost = cost
        self.material_type = material_type

    def get_material_cost(self) -> float:
        if self.material_type == "sand":
            return self.cost
        else:
            return self.cost * 1.5

def get_total_cost(self, material_list: List[DikeMaterial]) -> float:
    return max(_material.get_material_cost() for _material in material_list)

_material_list = [DikeMaterial(2.4, "sand"), DikeMaterial(4.2, "clay")]
get_total_cost(_material_list)

```
* We can do instead: 
```python
class DikeMaterial:
    def __init__(self, price: float):
        self.price = price

    def get_material_cost(self) -> float:
        return self.price

class ClayMaterial(DikeMaterial):
    def get_material_cost(self):
        return self.price * 1.5

_material_list = [Bridge(2.4), ClayMaterial(4.2)]
_costs = sum(_m.get_material_cost() for _m in material_list)
```

In addition, initaiting classes through _classmethods_, or external constructors / factories might allow you to easily create one or the other. Delegating even more responsibilities and being more aligned with the _Open-closed_ principle. Example:

```python
from typing import Protocol
from __future__ import annotations

class MaterialProtocol(Protocol):
    price: float
    name: str

    def get_cost(self) -> float:
        pass

class SandMaterial(MaterialProtocol):
    price: float

    def get_cost(self) -> float:
        return self.price * 1.14

    @classmethod
    def initiate_with_price(cls, price: float) -> Bridge:
        # Through class methods.
        _material = cls()
        _material.price = price
        return _material

def build_material(material_type: Type[MaterialProtocol], price: float) -> MaterialProtocol:
    # Through a 'builder'
    _material = bridge_type()
    _material.price = price
    return _material
```


### Liskov substitution.
A subclass must be substitutable by its super class. In my opinion, this principle is not really applyable in Python. Examples below:
```python
class SuperSand(SandMaterial):
    def get_cost(self) -> float:
        # Super taxed!
        return self.price * 2


_material = SuperSand.initiate_with_price(2)
# 1. First we prove the bridge is the same type as the base.
assert isinstance(_material, SandMaterial), "Failed principle!"

# 2. Then we prove the cost will be the same regardless of how it is typed (parent or subclass)
def get_as_sand_material(s_material: SandMaterial) -> float:
    return s_material.get_cost()

# To make it work, we should invoke 'super':
_m_cost = _material.get_cost()
assert get_as_sand_material(super(SuperSand, _material)) != _m_cost, "Failed principle!"
assert get_as_sand_material(_material) != _m_cost, "Failed principle!"
```

### Interface segregation principle.

Intefaces in Python are relatively "new", you can implement interfaces through `typing.Protocol`.

```python
from typing import List, Protocol, Tuple
from shapely.geometry import Point
from typing_extensions import runtime_checkable

@runtime_checkable
class DikeProfileProtocol(Protocol):
    characteristic_points: List[Point]
    height: float
    width: float

class DikeProfile(DikeProfileProtocol):
    ...

_dike = DikeProfile()
assert isinstance(_dike, DikeProfileProtocol)
# A protocol can't be instantiated, try this:
DikeProfileProtocol()
```
> Notice that the properties can be defined as inlines in the protocol. As long as they are declared later on (either with decorators or as inlines) the contract will be fulfilled.

> Pay attention as well to `@runtime_checkable`, it will allow us to verify whether an instance implements said protocol.

### Dependency inversion principle.
Depend on abstractions, not concretions.

```python
from matplotlib import pyplot
from shapely.geometry import LineString
from dikesfordummies.dike.dike_profile import DikeProfile

def _plot_line(ax, ob, color):
    parts = hasattr(ob, "geoms") and ob or [ob]
    for part in parts:
        x, y = part.xy
        ax.plot(x, y, color=color, linewidth=3, solid_capstyle="round", zorder=1)


def plot_profile(dike_profile: ReinforcementDikeProfile) -> pyplot:
    fig = pyplot.figure(1, dpi=90)
    _subplot = fig.add_subplot(221)
    _plot_line(
        _subplot, LineString(dike_profile.characteristic_points), color="#03a9fc"
    )
    return fig
```

In theory, the above code should only work for a ReinforcementDikeProfile, well, it's python so it will swallow also a regular profile. But we should aim to make the methods / classes depending on higher level of abstractions, so we could replace it with either the base class, or a protocol.

```python
def plot_profile(dike_profile: DikeProfile)
...
def plot_profile(dike_profile: DikeProfileProtocol)
```