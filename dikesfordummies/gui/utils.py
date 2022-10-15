from typing import Callable

from PyQt5 import QtWidgets


def create_menu_button(
    parent_window: QtWidgets.QWidget,
    pos: dict,
    title: str,
    tooltip: str,
    event: Callable,
    enabled: bool = True,
) -> QtWidgets.QPushButton:
    """
    Creates a QPushButton with the given parameters.

    Args:
        parent_window (QtWidgets.QWidget): QWidget which will contain the object to create.
        pos (dict): Dictionary with the 'ax', 'ay', 'aw' and 'az' values for setting the geometry.
        title (str): Text for the button to display.
        tooltip (str): Text for the button to display when hovering it.
        event (Callable): Method that will be called upon clicking on the button.
        enabled (bool, optional): Whether the button is enabled by defect. Defaults to True.

    Returns:
        QtWidgets.QPushButton: Created button.
    """
    _item_btn = QtWidgets.QPushButton(title, parent_window)
    _item_btn.setToolTip(tooltip)
    _item_btn.resize(_item_btn.sizeHint())
    _item_btn.setGeometry(pos["ax"], pos["ay"], pos["aw"], pos["az"])
    _item_btn.clicked.connect(event)
    if enabled:
        _item_btn.setEnabled(enabled)
    return _item_btn
