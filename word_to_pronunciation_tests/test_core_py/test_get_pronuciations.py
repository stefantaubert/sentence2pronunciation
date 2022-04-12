from word_to_pronunciation.core import get_pronunciations


def test_component():
  m = [
    [None, None],
    [(("a", "a"), 1.0), (("d", "d"), 3.0)],
    [(("b", "b"), 1.0), None],
    [None, (("d", "d"), 2.0)],
  ]

  result = list(get_pronunciations(m))

  assert result == [
    [tuple(), tuple()],
    [("a", "a"), ("d", "d")],
    [("b", "b"), tuple()],
    [tuple(), ("d", "d")],
  ]


def test_empty():
  result = list(get_pronunciations([]))
  assert result == []
