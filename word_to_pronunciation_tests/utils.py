
import random
import string

from word_to_pronunciation.types import Pronunciation


def random_string_generator(str_size: int, allowed_chars: str):
  return ''.join(random.choice(allowed_chars) for x in range(str_size))


chars = string.ascii_letters + string.punctuation


def get_random_sentence(words_count: int) -> Pronunciation:
  words = []
  for _ in range(words_count):
    words.append(random_string_generator(random.randint(3, 10), chars))
  return tuple(' '.join(words))
