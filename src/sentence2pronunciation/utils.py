from typing import Generator, List, Set, Tuple

from sentence2pronunciation.types import (Annotation, LookupMethod,
                                          Pronunciation, Pronunciations,
                                          Symbol, Symbols, Word)


def pronunciation_upper(pronunciation: Pronunciation) -> Pronunciation:
  result = tuple(symbol.upper() for symbol in pronunciation)
  return result


def pronunciation_lower(pronunciation: Pronunciation) -> Pronunciation:
  result = tuple(symbol.lower() for symbol in pronunciation)
  return result


def symbols_join(list_of_pronunciations: List[Pronunciation], join_symbol: Symbol) -> None:
  res = []
  for i, word in enumerate(list_of_pronunciations):
    res.extend(word)
    is_last_word = i == len(list_of_pronunciations) - 1
    if not is_last_word:
      res.append(join_symbol)
  return tuple(res)


# def symbols_split_iterable(sentence_symbols: Pronunciation, split_symbols: Set[Symbol]) -> Generator[Pronunciation, None, None]:
#   if len(sentence_symbols) == 0:
#     return
#   current = []
#   for symbol in sentence_symbols:
#     if symbol in split_symbols:
#       yield tuple(current)
#       current = []
#     else:
#       current.append(symbol)
#   yield tuple(current)


def separate_symbols(word: Word, symbols: Symbols) -> Tuple[Symbols, Word, Symbols]:
  beginning, remaining_word = separate_symbols_at_beginning(word, symbols)
  actual_word, end = separate_symbols_at_end(remaining_word, symbols)
  return beginning, actual_word, end


def separate_symbols_at_end(word: Word, symbols: Symbols) -> Tuple[Word, Symbols]:
  word_reversed = word[::-1]
  end_reversed, remaining_word_reversed = separate_symbols_at_beginning(
    word_reversed, symbols)
  end = end_reversed[::-1]
  remaining_word = remaining_word_reversed[::-1]
  return remaining_word, end


def separate_symbols_at_beginning(word: Word, symbols: Symbols) -> Tuple[Symbols, Word]:
  beginning = ""
  for element in word:
    if element in symbols:
      beginning += element
    else:
      break
  remaining_word = word[len(beginning):]
  return beginning, remaining_word
