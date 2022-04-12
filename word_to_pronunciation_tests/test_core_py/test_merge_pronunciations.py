from collections import OrderedDict

from word_to_pronunciation.core import merge_pronunciations


def test_component():
  parts = [
    None,
    OrderedDict((
      (("a", "b"), 1.0),
      (("c", "d"), 2.0),
    )),
    OrderedDict((
      (("e", "f"), 3.0),
    )),
    None,
  ]

  result = merge_pronunciations(parts, 0.5)

  assert result == OrderedDict((
    (("-", "a", "b", "-", "e", "f", "-"), 3.0),
    (("-", "c", "d", "-", "e", "f", "-"), 6.0),
  ))


def test_empty():
  result = merge_pronunciations([], 0.5)
  assert len(result) == 0


def test_None__returns_empty__default_weight():
  parts = [
    None,
  ]
  result = merge_pronunciations(parts, 0.5)
  assert result == OrderedDict((
    (tuple(), 0.5),
  ))


def test_None_None__returns_hyphen__default_weight():
  parts = [
    None,
    None,
  ]
  result = merge_pronunciations(parts, 0.5)
  assert result == OrderedDict((
    (("-",), 0.5),
  ))


def test_None_None_None__returns_hyphen_hypen__default_weight():
  parts = [
    None,
    None,
    None,
  ]
  result = merge_pronunciations(parts, 0.5)
  assert result == OrderedDict((
    (("-", "-"), 0.5),
  ))
