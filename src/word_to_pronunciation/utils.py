import re
from typing import Generator, List, Set, Tuple

from word_to_pronunciation.types import (Annotation, LookupMethod,
                                         Pronunciation, Pronunciations, Symbol,
                                         Symbols, Word)


def symbols_join(list_of_pronunciations: List[Pronunciation], join_symbol: Symbol) -> None:
  res = []
  for i, word in enumerate(list_of_pronunciations):
    res.extend(word)
    is_last_word = i == len(list_of_pronunciations) - 1
    if not is_last_word:
      res.append(join_symbol)
  return tuple(res)


def separate_symbols(word: Word, symbols: Symbols) -> Tuple[Symbols, Word, Symbols]:
  assert isinstance(word, str)
  assert isinstance(symbols, str)
  if symbols == "":
    return "", word, ""
  symbols_esc = re.escape(symbols)
  pattern = re.compile(rf"([{symbols_esc}]*)(.*)")
  res1 = re.match(pattern, word)
  assert res1 is not None
  start = res1.group(1)
  middle_tmp = res1.group(2)
  res2 = re.match(pattern, middle_tmp[::-1])
  assert res2 is not None
  middle = res2.group(2)[::-1]
  end = res2.group(1)[::-1]
  return start, middle, end
