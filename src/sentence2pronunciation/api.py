from collections import OrderedDict
from functools import partial
from typing import (Callable, Generator, Iterable, Iterator, List, Optional,
                    Set, Tuple)

from ordered_set import OrderedSet

from sentence2pronunciation.annotation_handling import (
    get_pronunciations_from_annotation, is_annotation)
from sentence2pronunciation.core import Options, word2pronunciation
from sentence2pronunciation.types import (Annotation, LookupMethod,
                                          Pronunciation, Pronunciations,
                                          Symbol, Symbols, Word)
from sentence2pronunciation.utils import separate_symbols, symbols_join


def get_pronunciations_from_word(word: Word, lookup: LookupMethod, options: Options) -> Pronunciations:
  if options.consider_annotation and len(options.annotation_split_symbol) != 1:
    raise ValueError("annotation_split_symbol has to be a string of length 1.")
  return word2pronunciation(word, lookup, options)
