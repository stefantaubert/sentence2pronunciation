from collections import OrderedDict

from word_to_pronunciation.core import get_matrix


def test_empty__returns_empty():
  res = get_matrix([])
  assert res == []


def test_None__returns_None():
  res = get_matrix([None])
  assert res == [[None]]


def test_one_entry__returns():
  res = get_matrix([OrderedDict((
    (("a",), 1.0),
  ))])
  assert res == [[(("a",), 1.0)]]


def test_one_entry_None__returns():
  res = get_matrix([
    OrderedDict((
      (("a",), 1.0),
    )),
    None,
  ])
  assert res == [
    [(("a",), 1.0), None],
  ]


def test_None_entry__returns():
  res = get_matrix([
    None,
    OrderedDict((
      (("a",), 1.0),
    )),
  ])
  assert res == [
    [None, (("a",), 1.0)],
  ]


def test_None_entry1_entry1__returns_None_entry_1_entry_1():
  res = get_matrix([
    None,
    OrderedDict((
      (("a",), 1.0),
    )),
    OrderedDict((
      (("a",), 1.0),
    )),
  ])
  assert res == [
    [None, (("a",), 1.0), (("a",), 1.0)],
  ]


def test_None_entryA_B__returns_None_entryA__None_entryB():
  res = get_matrix([
    None,
    OrderedDict((
      (("a",), 1.0),
      (("b",), 1.0),
    )),
  ])
  assert res == [
    [None, (("a",), 1.0)],
    [None, (("b",), 1.0)],
  ]


def test_entryA_B__None__returns_entryA_None__entryB_None():
  res = get_matrix([
    OrderedDict((
      (("a",), 1.0),
      (("b",), 1.0),
    )),
    None,
  ])
  assert res == [
    [(("a",), 1.0), None],
    [(("b",), 1.0), None],
  ]


def test_A_B__C_D__returns__A_C__A_D__B_C__B_D():
  res = get_matrix([
    OrderedDict((
      (("a",), 1.0),
      (("b",), 1.0),
    )),
    OrderedDict((
      (("c",), 1.0),
      (("d",), 1.0),
    )),
  ])

  assert res == [
    [(("a",), 1.0), (("c",), 1.0)],
    [(("a",), 1.0), (("d",), 1.0)],
    [(("b",), 1.0), (("c",), 1.0)],
    [(("b",), 1.0), (("d",), 1.0)],
  ]


def test_AA_BB__CC_DD__returns__AA_CC__AA_DD__BB_CC__BB_DD():
  res = get_matrix([
    OrderedDict((
      (("a", "a"), 1.0),
      (("b", "b"), 1.0),
    )),
    OrderedDict((
      (("c", "c"), 1.0),
      (("d", "d"), 1.0),
    )),
  ])

  assert res == [
    [(("a", "a"), 1.0), (("c", "c"), 1.0)],
    [(("a", "a"), 1.0), (("d", "d"), 1.0)],
    [(("b", "b"), 1.0), (("c", "c"), 1.0)],
    [(("b", "b"), 1.0), (("d", "d"), 1.0)],
  ]
