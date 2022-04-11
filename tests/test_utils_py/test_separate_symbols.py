
from word_to_pronunciation.utils import separate_symbols


def test_empty_empty__returns_empty_empty_empty():
  start, middle, end = separate_symbols("", "")
  assert start == ""
  assert middle == ""
  assert end == ""


def test_a_empty__returns_empty_a_empty():
  start, middle, end = separate_symbols("a", "")
  assert start == ""
  assert middle == "a"
  assert end == ""


def test_empty_X__returns_empty_empty_empty():
  start, middle, end = separate_symbols("", "X")
  assert start == ""
  assert middle == ""
  assert end == ""


def test_X_X__returns_X_empty_empty():
  start, middle, end = separate_symbols(".", ".")
  assert start == "."
  assert middle == ""
  assert end == ""


def test_Xa_X__returns_X_a_empty():
  start, middle, end = separate_symbols("Xa", "X")
  assert start == "X"
  assert middle == "a"
  assert end == ""


def test_XaX_X__returns_X_a_X():
  start, middle, end = separate_symbols("XaX", "X")
  assert start == "X"
  assert middle == "a"
  assert end == "X"


def test_aX_X__returns_empty_a_X():
  start, middle, end = separate_symbols("aX", "X")
  assert start == ""
  assert middle == "a"
  assert end == "X"


def test_component():
  start, middle, end = separate_symbols(".?abc-de!-.", ".!?-")
  assert start == ".?"
  assert middle == "abc-de"
  assert end == "!-."
