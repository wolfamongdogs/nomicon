from rules import VowelsToNumbersChanger, PopularSuffixAdder, AToSymbolsChanger
from rules import SToDollarSignChanger, CapitalLetterIntroducer, DateAdder
from rules import SymbolChanger, TitlecaseChanger, CaseInverter, WordUpcaserDowncaser

# Add transformers in an array with the arguments their init methods need MINUS the password
# Password always needs to come last
transformers = [
    [VowelsToNumbersChanger, 'aeioAEIO', ''],
    [PopularSuffixAdder],
    [AToSymbolsChanger, 'Aa', ''],
    [SToDollarSignChanger, 'sS', '$'],
    [CapitalLetterIntroducer],
    [DateAdder],
    [SymbolChanger, '&+!?', ''],
    [TitlecaseChanger],
    [WordUpcaserDowncaser],
    [CaseInverter],
]
