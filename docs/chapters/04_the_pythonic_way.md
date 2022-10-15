# Chapter 04. The pythonic way.
Catching up? Just run the following command in your command line:
```bash
conda env create -f environment.yml
conda activate dikes-for-dummies_env
poetry install
```
You can follow the contents of this chapter now :)

## Intro
Because we are doing OO in python it is also useful to learn certain Python techniques that can be handy specially when dealing with large amounts of data.

-- "Ask for forgiveness, not for permission" --

Let's '_pythonize_' the following snippet.

```python
from typing import List, Tuple
from shapely.geometry import Point

def get_as_points_if_even(tuple_points: List[Tuple[float]]) -> List[Point]:
    def is_even(number: float) -> bool:
        return number % 2 == 0

    _list = []
    for p_tuple in tuple_points:
        if is_even(p_tuple[0]) and is_even(p_tuple[1]):
            _list.append(Point(p_tuple))
    return _list

_points = get_as_points_if_even([(1, 1), (2, 4), (3, 7), (4, 10)])
```

## List comprehensions.

```python
def get_as_points_if_even(tuple_points: List[Tuple[float]]) -> List[Point]:
    def is_even_tuple(p_tuple: Tuple[float]) -> bool:
        return all(_p % 2 == 0 for _p in p_tuple)

    return [Point(p_tuple) for p_tuple in tuple_points if is_even_tuple(p_tuple)]
```

## Filter.

Returns an iterable when a condition is met.:

```python
def get_as_points_if_even(tuple_points: List[Tuple[float]]) -> List[Point]:
    def is_even_tuple(p_tuple: Tuple[float]) -> bool:
        return all(_p % 2 == 0 for _p in p_tuple)

    return [Point(p_tuple) for p_tuple in filter(tuple_points)]
```

## Map.

Returns an iterable of a callable applied in a collection of items:

```python
def get_as_points_if_even(tuple_points: List[Tuple[float]]) -> Iterable[Point]:
    def is_even_tuple(p_tuple: Tuple[float]) -> bool:
        return all(_p % 2 == 0 for _p in p_tuple)

    return map(Point, filter(is_even_tuple, tuple_points))

_points = list(get_as_points_if_even([(1, 1), (2, 4), (3, 7), (4, 10)]))
```

## Zip.

Returns an iterable of paired tuples:

```python
_coords = range(1, 12)
_x_points = _coords[:4]
_y_points = _coords[0::3]
_points = list(get_as_points_if_even(zip(_x_points, _y_points)))
```

## Lambda functions.

A lambda expression is nothing else than a 'inline method', we can use it in combination of the above generators / iterables.

```python
_points: Iterator[Point] = get_as_points_if_even(zip(_x_points, _y_points))
# We are going to increment the y coordinates by two values:
_new_points = list(map(lambda _p: Point(_p.x, _p.y + 2), _points))
```

Iterators are 'consumed'. Once you iterate over them they will no longer contain data. Check what happens when you inspect `_points` now.

```python
# These asserts are equivalent under Python's eyes.
assert not _points
assert len(_points) == 0
```

## Dictionaries. 

Very helpful in many ways, you can use it to store any kind of callable, iterable or python object and iterate over the entire collection.

Some basic snippets:
* Declaring a dictionary:
    ```python
    simple_dict = {"a": 123}
    # or
    simple_dict = dict(a=123)
    # but for both is possible:
    simple_dict["b"] = 456
    ```
* Accessing a dictionary:
    ```python
    assert simple_dict.keys() == ["a", "b"]
    assert simple_dict.values() == [123, 456]
    assert simple_dict.items() == [("a", 123), ("b", 456)]
    # this will raise:
    _c_value = simple_dict["c"]
    # But this don't:
    _c_value = simple_dict.get("c", None)
    ```
* Providing the contents of a dictionary:
    ```python
    _profile_data = dict(points=_points, name="A Test Dike")
    class DikeProfile:
        points: List[Point]
        name: str

        def __init__(self, points: List[Point], name: str) -> None:
            self.points = points
            self.name = name

    _profile = DikeProfile(**_profile_data)
    ```
* Assigning the values of a dictionary directly to a class:
    ```python
    class DikeProfile:
        points: List[Point]
        name: str

        def __init__(self) -> None:
            self.points = []
            self.name = ""

        @classmethod
        def with_data_dict(cls, data_dict: dict) -> DikeProfile:
            _profile = cls()
            _profile.__dict__ = data_dict
            return _profile


    _profile = DikeProfile.with_data_dict(dict(points=_points, name="A Test Dike"))
    assert isinstance(_profile, DikeProfile)
    ```

## Logging

It is quite common wanting to log the different steps or actions throughout your entire solution. This can easily be achieved with the library `logging`.

```python
import logging

# Defining our logger.
_logger = logging.getLogger("")
_logger.setLevel(logging.DEBUG)

# Defining our custom formatter
_formatter = logging.Formatter(
    fmt="%(asctime)s - [%(filename)s:%(lineno)d] - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S %p",
)

# Adding a console handler
_console_handler = logging.StreamHandler()
_console_handler.setLevel(logging.INFO)
_console_handler.setFormatter(_formatter)
_logger.addHandler(_console_handler)

# Adding a file handler.
_log_file = Path(__file__).parent / "dikes_for_dummies.log"
_file_handler = logging.FileHandler(filename=_log_file, mode="w")
_file_handler.setLevel(logging.INFO)
_file_handler.setFormatter(_formatter)
_logger.addHandler(_file_handler)
```

## Disposable classes.
A nice technique when wanting to create `disposable` objects that should realize initialization and finalize operations during a very specific period can be achieved with `__enter__` and `__exit__`. A good example of this are file streams. But you may also think of your own logging (instead of default library `logging`) or your own wrappers around runners.

Example for a logger:
```python

class ExternalRunnerLogging:
    ...
    def __enter__(self) -> None:
        _runner_name = self._get_runner_name()

        self._wrap_message(f"Initialized Runner Logging for {_runner_name}")

    def __exit__(self, *args, **kwargs) -> None:
        _logger = logging.getLogger("")
        _runner_name = self._get_runner_name()
        self._wrap_message(f"Logger terminated for {_runner_name}")
        _logger.removeHandler(self._file_handler)
```
And its usage:

```python
def run(self):
    ...
    with ExternalRunnerLogging(self):
        ...
        try:
            ...
        except Exception as exc:
            logging.info(f"Error during runner execution {exc}")
            ...
```

