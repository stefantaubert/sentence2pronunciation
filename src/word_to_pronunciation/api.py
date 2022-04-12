from collections import OrderedDict
from functools import partial
from logging import getLogger
from typing import Dict

from word_to_pronunciation.core import Options, word2pronunciation
from word_to_pronunciation.types import LookupMethod, Pronunciations, Word


def get_pronunciations_from_word(word: Word, lookup: LookupMethod, options: Options) -> Pronunciations:
  internal_lookup_method = partial(
    lookup_with_check,
    lookup=lookup,
  )

  return word2pronunciation(word, internal_lookup_method, options)


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


def lookup_with_check(word: Word, lookup: LookupMethod) -> Pronunciations:
  logger = getLogger(__name__)
  try:
    result = lookup(word)
  except Exception as ex:
    logger.warning("Lookup method raised an exception!")
    logger.debug(ex)
    return OrderedDict()

  if not isinstance(result, OrderedDict):
    logger.warning("Lookup method returned an invalid pronunciation!")
    return OrderedDict()

  for k, v in result.items():
    if not isinstance(k, tuple) or not len(k) > 0:
      logger.warning("Lookup method returned an invalid pronunciation!")
      logger.debug(result)
      return OrderedDict()
    if not (isinstance(v, float) or isinstance(v, int)):
      logger.warning("Lookup method returned an invalid pronunciation weight!")
      logger.debug(result)
      return OrderedDict()

  return result
