# Chapter 02. Never trust the user.

__Why you should never trust the user and their given input__
Unlike other OO languages, Python has `duck typing` and is a dynamic language.
This means that even if you declared in a method that you want an object of type `Banana` you may end up getting `Peanuts` instead.
For this reason, I always advice **never** to trust the user.

However, as seen in the previous chapter, we have different ways of distributing the package. We will see what this means by the [end of the chapter](#summary).

We are going to start debugging some snippets in this chapter to get a grip of some python concepts, so, let's add a `launch.json` to our `.vscode` directory.

## Methods in Python
These are ways of declaring methods and handling their input / output. Try them out.

```python
def get_dike_profile_points():
    return None
get_dike_profile_points()
```

```python
def get_dike_profile_points(*args, **kwargs):
    return (1,2)
x = get_dike_profile_points(abc=(3,4,5))
x1, x2 = x
```

```python
def get_dike_profile_points(abc, *args, **kwargs):
    return ((1,2), (3,4), (5,6))
p1, p2 , p3= get_dike_profile_points(3,4,5)
```

As can be seen, we can collect the parameters declaring them explicetly or by using the parameters `*args` or `**kwargs`.

## Classes in Python
Official reference https://docs.python.org/3/tutorial/classes.html.

Creating classes is very simple, you just need to add the `class` type at its begining:

```python
class DikeProfile:
    pass
```

We can also apply (multiple) inheritance.

```python
class SoilReinforcementProfile(DikeProfile):
    pass
```

### Initialization.

We initializing classes usually with the `def __init__(self, *args, **kwargs)` method. However we can take different approaches.

- Default constructor:
```python
class DikeProfile:
    def __init__(self, *args, **kwargs):
        self.name = "A default Dike Profile"
_dike_profile = DikeProfile()
```
 - From a class method (later further explained):

```python
class DikeProfile:
    @classmethod
    def from_data_dict(cls, **kwargs):
        _dike_profile = cls()
        _dike_profile.name = kwargs.get("name", "A default Dike Profile")
        return _dike_profile
_dike_profile = DikeProfile.from_data_dict(name="Or not so default.")
```

 - From a 'builder' (or a _FactoryPattern_):

```python
 class DikeProfileBuilder:
    def build(self):
        _profile = DikeProfile()
        _profile.name = "A default Dike Profile"
        return _profile
```

There are certain libraries that help initializing classes while enforcing its typing. Have a look at [Pydantic](https://pydantic-docs.helpmanual.io/). Keep in mind that when using such libraries you are constrained to their potential bugs / limitations. So you should be responsible on to how to use it (later discussed in the [summary](#summary)).

### Static methods.
These are examples of static methods:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# outside a class
def get_tuple_as_point( x, y):
    return Point(x, y)

_point = get_tuple_as_point(4, 2)
# In a class with decorator staticmethod
class DikeProfileBuilder:
    @staticmethod
    def get_point_list(*args, **kwargs):
        _point_list = []
        for point_tuple in args:
            x, y = point_tuple
            _point_list.append(get_tuple_as_point(x, y))
        return _point_list
_point_list = DikeProfileBuilder.get_point_list((4, 2), (2,4))
```

### Class methods.
A class method is similar to a static one. However, despite being technically possible to make them behave identically, a class method is meant to return an instance of the class being invoked.

```python
# Do not:
class DikeProfile:
    @classmethod
    def get_point_list(cls, *args, **kwargs):
        pass
# Do:
def get_point_list(*args):
    pass
class DikeProfile:
    @classmethod
    def from_data(cls, *args, **kwargs):
        _dike_profile = cls()
        _dike_profile.points = get_point_list(args)
        return _dike_profile
_profile = DikeProfile.from_data((1,2), (3,4))
```

### Overloading methods.
As in other OO languages, we can also overload methods:

```python
class DikeProfile:
    def __str__(self):
        return "A default DikeProfile"
print(str(DikeProfile()))
```
And of course, we can also overload [operators](https://docs.python.org/3/library/operator.html):
```python
class DikeProfile:
    def __eq__(self, compare_to):
        if len(compare_to.points) != len(self.points):
            return False
        for idx, point in enumerate(self.points):
            to_point = compare_to.pints[idx]
            if to_point.x != point.x or to_point.y != point.y:
                return False
        return True

_dike_a = DikeProfile()
_dike_a.points = [Point(1, 2), Point(2, 3)]
_dike_b = DikeProfile()
_dike_b.points = [Point(1, 2), Point(2, 3)]
assert _dike_a == _dike_b
_dike_b.points = [Point(1, 2), Point(2, 4)]
assert _dike_a != _dike_b
```

### Handling errors:
Some examples on how to handle errors in Python:
```python
try:
    _result = 1 / 0
except Exception as exc_info:
    ...
finally:
    ...
```

```python
from pathlib import Path
def read_file(file):
    if not file:
        raise ValueError("File not provided")
    if not isinstance(file, Path):
        file = Path(file)
    if not file.is_file():
        # This error is futile as the built-in read_text would raise it anyway.
        raise FileNotFoundError(f"File not found at {file}")
    _lines = file.read_text().splitlines(keepends=False)
```

## Clean code (or the most effective ways to make it clean).
This part ends up being more a responsibility than a mechanism we can build (except for certain code formatters.) The first advice, is to adhere to the following:
* Dry code.
* Single responsibility principle (OO).
* Classes and methods standardization.
    - Use code formatters and related tools, the most simple one `black`.
   ```console
    poetry run black .
   ```
    - You can also order your imports with `isort`.
   ```console
    poetry run isort .
   ```
* Descriptive (consistent) variables.
   ```python
    # Don't
    _mcf = a_calculation_that_happens_somewhere(a,b)
    # Do
    _geometry_area = calculate_geometry(_list_of_points)
   ```
* Documented code.
    - [Type hinting](https://docs.python.org/3/library/typing.html)
   ```python
    from __future__ import annotations

    from typing import List, Tuple


    class Point:
        x: float
        y: float

        def __init__(self, x: float, y: float) -> None:
            self.x = x
            self.y = y

        def __str__(self) -> str:
            return f"Point ({self.x}, {self.y})"


    class DikeProfile:
        def __init__(self):
            self._points = []

        @classmethod
        def with_data(cls, point_tuples: List[Tuple[float]]) -> DikeProfile:
            _profile = cls()
            _profile.points = [Point(*_pt) for _pt in point_tuples]
            return _profile

        @property
        def points(self) -> List[Point]:
            return self._points

        @points.setter
        def points(self, list_values: List[Point]):
            self._points = list_values


    _dike = DikeProfile.with_data([(1, 2), (2, 3)])
    for point in _dike.points:
        print(point)
   ```
    - Docstrings (pick your preferred format and be __consistent__ about it). When using autoDocstring, you only need to write three " and press enter to generate a template.

   ```python
    class DikeProfile:
        pass
    class DikeReinforcementInput:
        pass
    class ReinforcedDikeProfile(DikeProfile):
        pass

    def profile_calculator(profile: DikeProfile, new_input: DikeReinforcementInput) -> ReinforcedDikeProfile:
        """
        Calculates a new profile based on the given `profile` and `new_input`.

        Args:
            profile (DikeProfile): Base profile on which calculations will be done.
            new_input (DikeReinforcementInput): Data input required to perform calculations.

        Returns:
            ReinforcedDikeProfile: Instance of new reinforced Dike
        """
        pass
   ```

## Summary

In this chapter we have seen that in Python we can still code in an effective Object Oriented way.

However, as mentioned, because of Python being a dynamic language, and the ways of distributing the repository, we need to consider also how to handle potential errors in the code and / or users' input. Let's analyze the options:
1. As a package library (pip) or sandbox. 
    1. The user is an 'expert' or a 'developer'. 
    2. The code contains type-hints and tests ensuring the correct functioning.
    3. We only try-catch on high end operations or as a part of a wrapper to a third-party package.

2. As an endpoint, CLI, API or .exe product.
    1. The user does not necessairly need to know how to code.
    2. The user only uses the API endpoints / calls which are well-documented.
    
In 1.1 the user should be responsible enough to know how to handle the package. It should be accepted to just follow a __fail-fast__ philosophy in our code. However, in the second case, we could do error handling at a higher level (classic main.py) yet leaving the rest of the code intentionally following a fail-fast philosophy.
