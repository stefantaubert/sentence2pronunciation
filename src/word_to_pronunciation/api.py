from functools import partial
from typing import Dict

from word_to_pronunciation.core import Options, word2pronunciation
from word_to_pronunciation.types import LookupMethod, Pronunciations, Word


def get_pronunciations_from_word(word: Word, lookup: LookupMethod, options: Options) -> Pronunciations:
  return word2pronunciation(word, lookup, options)


def get_cached_lookup(lookup: LookupMethod, cache: Dict[Word, Pronunciations]) -> LookupMethod:
  result = partial(
    lookup_cached,
    lookup=lookup,
    cache=cache,
  )
  return result


def lookup_cached(word: Word, lookup: LookupMethod, cache: Dict[Word, Pronunciations]) -> Pronunciations:
  if word in cache:
    return cache[word]
  else:
    result = lookup(word)
    cache[word] = result
    return result
