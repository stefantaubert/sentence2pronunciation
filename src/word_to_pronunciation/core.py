from collections import OrderedDict
from dataclasses import dataclass
from functools import partial
from typing import (Callable, Dict, Generator, Iterable, Iterator, List,
                    Optional, Set, Tuple)

from ordered_set import OrderedSet

from word_to_pronunciation.annotation_handling import (
    get_pronunciations_from_annotation, is_annotation)
from word_to_pronunciation.types import (Annotation, LookupMethod,
                                         Pronunciation, Pronunciations, Symbol,
                                         Symbols, Word)
from word_to_pronunciation.utils import separate_symbols, symbols_join

HYPHEN = "-"


@dataclass()
class Options():
  trim_symbols: Symbols
  split_on_hyphen: bool
  consider_annotation: bool
  annotation_split_symbol: Optional[Symbol]
  try_without_trimming: bool
  try_without_splitting: bool
  # use this weight for annotations and words consisting only of trim_symbols
  default_weight: Optional[float]


def word2pronunciation(word: Word, lookup: LookupMethod, options: Options) -> Pronunciations:
  assert isinstance(word, str)
  assert isinstance(options, Options)

  if options.consider_annotation:
    assert options.annotation_split_symbol is not None
    assert options.default_weight is not None

  if word == "":
    return OrderedDict()

  if options.consider_annotation and is_annotation(word, options.annotation_split_symbol):
    annotation = word
    result = get_pronunciations_from_annotation(
      annotation, options.annotation_split_symbol, options.default_weight)
    return result

  if len(options.trim_symbols) > 0 and options.try_without_trimming:
    lookup_result = lookup(word)

    if len(lookup_result) > 0:
      return lookup_result

  if len(options.trim_symbols) > 0:
    trim_beginning, word_core, trim_end = separate_symbols(word, options.trim_symbols)
    contains_only_punctuation = word_core == ""
    if contains_only_punctuation:
      assert trim_end == ""
      assert trim_beginning == word
      pronunciation = tuple(word)
      result = OrderedDict((
        (pronunciation, options.default_weight),
      ))
      return result
  else:
    trim_beginning = ""
    word_core = word
    trim_end = ""

  if options.split_on_hyphen and options.try_without_splitting:
    lookup_result = lookup(word_core)

    if len(lookup_result) > 0:
      result = join_begin_and_end(lookup_result, trim_beginning, trim_end)
      return result

  if options.split_on_hyphen:
    words = word_core.split(HYPHEN)
    resulting_pronunciations = []
    for w in words:
      if w == "":
        resulting_pronunciations.append(None)
      else:
        lookup_result = lookup(w)
        if len(lookup_result) == 0:
          return lookup_result
        resulting_pronunciations.append(lookup_result)
    result = merge_pronunciations_together(resulting_pronunciations)
  else:
    lookup_result = lookup(word_core)

  result = join_begin_and_end(lookup_result, trim_beginning, trim_end)
  return result


def join_begin_and_end(pronunciations: Pronunciations, beginning: str, end: str) -> Pronunciations:
  if beginning == "" and end == "":
    return pronunciations

  result = OrderedDict()
  beginning_list = list(beginning)
  ending_list = list(end)
  for pronunciation, weight in pronunciations.items():
    new_pronunciation = beginning_list + list(pronunciation) + ending_list
    new_pronunciation = tuple(new_pronunciation)
    result[new_pronunciation] = weight
  return result


def merge_pronunciations_together(parts: List[Optional[Pronunciations]]) -> Pronunciations:
  tmp: List[Symbol] = []
  weights = []
  for part in parts:
    new_tmp = []
    new_weights = []
    if part is None:
      for entry in tmp:
        new_entry = entry + [tuple()]
        new_tmp.append(new_entry)
      tmp = new_tmp
    else:
      assert len(part) > 0
      for entry, weight in zip(tmp, weights):
        for entry2, weight2 in part.items():
          new_entry = entry + list(entry2)
          new_weight = weight * weight2
        new_tmp.append(new_entry)
        new_weights.append(new_weight)
      tmp = new_tmp
      weights = new_weights
  assert len(tmp) == len(weights)
  new_tmp = (
    symbols_join(entry, HYPHEN)
    for entry in tmp
  )
  result = OrderedDict(zip(tmp, weights))
  return result
