import re
from typing import Callable, Dict, List, Optional, Set, Tuple

Pronun = Tuple[str, ...]
Pronun_Dict = Dict[str, Pronun]


def sentence2pronunciaton(sentence: str, trim_symb: Set[str], split_on_hyphen: bool, get_pronun: Callable[[str], Pronun], cons_annotation: bool, annotation_split_symbol: Optional[str] = None) -> Pronun:
  words = sentence.split(" ")
  pronuns = []
  for word in words:
    word_or_annotation2pronunciation(
      word, pronuns, trim_symb, split_on_hyphen, get_pronun, cons_annotation, annotation_split_symbol)
  # -1 because there is one unneccessary space at the end
  complete_pronun = pronunlist_to_pronun(pronuns[:-1])
  return complete_pronun


def word_or_annotation2pronunciation(word: str, pronuns: List[Pronun], trim_symb: Set[str], split_on_hyphen: bool, get_pronun: Callable[[str], Pronun], cons_annotation: bool, annotation_split_symbol: Optional[str] = None) -> None:
  if cons_annotation and is_annotation(word, annotation_split_symbol):
    annotations = annotation2pronunciation(word, annotation_split_symbol)
    pronuns.append(annotations)
  else:
    new_pronun = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)
    pronuns.append(new_pronun)
  pronuns.append((" ",))


def is_annotation(word: str, annotation_split_symbol: str) -> bool:
  annot = re.compile(rf"{annotation_split_symbol}[\S]+{annotation_split_symbol}\Z")
  poss_annot = annot.match(word)
  return not(poss_annot is None)


def annotation2pronunciation(annot: str, annotation_split_symbol: str) -> Pronun:
  assert is_annotation(annot, annotation_split_symbol)
  single_annots = re.findall(rf"[^{annotation_split_symbol}]+", annot)
  single_annots = tuple(single_annots)
  return single_annots


def word2pronunciation(word: str, trim_symb: Set[str], split_on_hyphen: bool, get_pronun: Callable[[str], Pronun]) -> Pronun:
  trim_beginning, act_word, trim_end = trim_word(word, trim_symb)
  pronuns = [(trim_beginning,)]
  add_pronun_for_word(pronuns, act_word, split_on_hyphen, get_pronun)
  pronuns.append((trim_end,))
  complete_pronun = pronunlist_to_pronun(pronuns)
  return complete_pronun


def add_pronun_for_word(pronuns: List[Pronun], word: str, split_on_hyphen: bool, get_pronun: Callable[[str], Pronun]) -> None:
  if split_on_hyphen:
    splitted_words = word.split("-")
    for index, single_word in enumerate(splitted_words):
      pronuns.append(get_pronun(single_word))
      if index != len(splitted_words) - 1:
        pronuns.append(("-",))
  else:
    pronuns.append(get_pronun(word))


def trim_word(word: str, trim_symb: Set[str]) -> Tuple[str, str, str]:
  trim_symb_single_str = "".join(str(symb) for symb in trim_symb)
  trim = re.compile(rf"[{trim_symb_single_str}]*")
  beginning = trim.match(word).group(0)
  reverse_word = word[::-1]
  end = trim.match(reverse_word).group(0)
  end = end[::-1]
  if end != "":
    act_word = word[len(beginning):-len(end)]
  else:
    act_word = word[len(beginning):]
  return beginning, act_word, end


# def get_pronun(word: str, dict: Pronun_Dict, replace_unknown_with) -> Pronun:
#  if word in dict.keys():
#    return dict[word]
#  return replace_unknown_with * len(word)


def pronunlist_to_pronun(pronunlist: List[Pronun]) -> Pronun:
  for ele in pronunlist:
    assert isinstance(ele, tuple)
  flattened_pronunlist = [
    pronun for pronuntuple in pronunlist for pronun in pronuntuple if pronun != ""]
  return tuple(flattened_pronunlist)
