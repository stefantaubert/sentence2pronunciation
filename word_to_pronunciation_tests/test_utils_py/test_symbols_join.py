from word_to_pronunciation.utils import symbols_join


def test_empty__X__returns_empty():
  result = tuple(symbols_join([], "X"))
  assert result == tuple()


def test_empty__empty__returns_empty():
  result = tuple(symbols_join([], ""))
  assert result == tuple()


def test_empty__None__returns_empty():
  result = tuple(symbols_join([], None))
  assert result == tuple()


def test_empty_tuple__X__returns_empty_tuple():
  result = tuple(symbols_join([tuple()], "X"))
  assert result == tuple()


def test_empty_tuple__empty_tuple__X__returns_empty_tuple_X_empty_tuple():
  result = tuple(symbols_join([tuple(), tuple()], "X"))
  assert result == ("X",)


def test_a__X__returns_a():
  result = tuple(symbols_join([("a",)], "X"))
  assert result == ("a",)


def test_a__a__X__returns_aXa():
  result = tuple(symbols_join([("a",), ("a",)], "X"))
  assert result == ("a", "X", "a")


def test_a_b__c__X__returns_abXc():
  result = tuple(symbols_join([("a", "b"), ("c",)], "X"))
  assert result == ("a", "b", "X", "c")


def test_aa_bb__cc__X__returns_aabbXcc():
  result = tuple(symbols_join([("aa", "bb"), ("cc",)], "X"))
  assert result == ("aa", "bb", "X", "cc")
