from collections import OrderedDict

from iterable_serialization import deserialize_iterable

from word_to_pronunciation.types import (Annotation, LookupMethod,
                                         Pronunciation, Pronunciations, Symbol,
                                         Symbols, Word)


def is_annotation(word: Word, annotation_split_symbol: Symbol) -> bool:
  assert len(annotation_split_symbol) == 1
  return len(word) >= 3 and word[0] == annotation_split_symbol and word[-1] == annotation_split_symbol


def get_pronunciations_from_annotation(annotation: Annotation, annotation_split_symbol: Symbol, annotation_weight: float) -> Pronunciations:
  assert is_annotation(annotation, annotation_split_symbol)
  pronunciation = get_annotation_content(annotation, annotation_split_symbol)
  result = OrderedDict((
    (pronunciation, annotation_weight),
  ))
  return result


def get_annotation_content(annotation: Annotation, annotation_split_symbol: Symbol) -> Pronunciation:
  assert is_annotation(annotation, annotation_split_symbol)
  annotation_content = annotation[1:-1]
  assert len(annotation_content) > 0
  pronunciation = tuple(deserialize_iterable(annotation_content, annotation_split_symbol))
  return pronunciation
