from collections import OrderedDict

from word_to_pronunciation.core import Options, word2pronunciation
from word_to_pronunciation.types import Pronunciations


def dummy_lookup(word: str) -> Pronunciations:
  pronunciation = tuple(
    f"{symbol}{symbol}" for symbol in word
  )
  result = OrderedDict((
    (pronunciation, 1.0),
  ))
  return result


def test_empty_empty__returns_empty():
  word = ""
  options = Options("", False, False, False, 1.0)
  result = word2pronunciation(word, dummy_lookup, options)
  assert len(result) == 0


def test_a_empty__returns_aa():
  word = "a"
  options = Options("", False, False, False, 1.0)
  result = word2pronunciation(word, dummy_lookup, options)
  assert len(result) == 1
  assert result[("aa",)] == 1.0


def test_empty_X__returns_empty():
  word = ""
  options = Options("X", False, False, False, 1.0)
  result = word2pronunciation(word, dummy_lookup, options)
  assert len(result) == 0


def test_X_X__returns_X():
  word = "X"
  options = Options("X", False, False, False, 1.0)
  result = word2pronunciation(word, dummy_lookup, options)
  assert len(result) == 1
  assert result[("X",)] == 1.0


def test_aa__returns_aa_aa():
  word = "aa"
  options = Options("", False, False, False, 1.0)
  result = word2pronunciation(word, dummy_lookup, options)
  assert len(result) == 1
  assert result[("aa", "aa")] == 1.0


def test_aX_X__returns_aa_X():
  word = "aX"
  options = Options("X", False, False, False, 1.0)
  result = word2pronunciation(word, dummy_lookup, options)
  assert len(result) == 1
  assert result[("aa", "X")] == 1.0


def test_aaX_X__returns_aa_aa_X():
  word = "aaX"
  options = Options("X", False, False, False, 1.0)
  result = word2pronunciation(word, dummy_lookup, options)
  assert len(result) == 1
  assert result[("aa", "aa", "X")] == 1.0
