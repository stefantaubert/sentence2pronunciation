from word_to_pronunciation.core import get_weights


def test_component():
  m = [
    [None, None],
    [(("a", "a"), 1.0), (("d", "d"), 3.0)],
    [(("b", "b"), 1.0), None],
    [None, (("d", "d"), 2.0)],
  ]

  result = list(get_weights(m))

  assert result == [None, 3.0, 1.0, 2.0]


def test_empty():
  result = list(get_weights([]))
  assert result == []
