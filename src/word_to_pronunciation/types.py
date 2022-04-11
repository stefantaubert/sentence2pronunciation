from collections import OrderedDict
from typing import Callable
from typing import OrderedDict as OrderedDictType
from typing import Tuple

Symbol = str
Symbols = str
Word = str
Annotation = str
Pronunciation = Tuple[Symbol, ...]
Weight = float
Pronunciations = OrderedDictType[Pronunciation, Weight]
LookupMethod = Callable[[Word], Pronunciations]
