import utilities
from datetime import date


class RuleGenerator:

    flag = "set this to flag"

    def __init__(self, chars, change_char="", pwd=""):
        self.chars = chars
        self.pwd = pwd
        self.change_char = change_char

    def description(self):
        return ("""
        Overwrite this function so you can have a description of what this does.
        """)

    def change_function(self, char, change):
        if char in self.chars and change == "1":
            return self.change_char
        else:
            return char

    def mutate(self, pwd_to_change=None):
        pwd_to_change = pwd_to_change or self.pwd
        pwds = utilities.set_up_and_Change_characters(self.chars,
                                                      pwd_to_change,
                                                      self.change_function)
        return (pwds)


class DateAdder(RuleGenerator):

    flag = "-d"

    def __init__(self, pwd):
        self.pwd = pwd

    def generate_dates(self):
        current_year = date.today().year
        dates = []
        for n in range(6):
            dates.append(int(current_year) - n)

        return dates

    def description(self):
        return ("""
        -d      This adds the current date as well as 5 years previous
                to the front and back of the password.
        """)

    def mutate(self, pwd_to_change=None):
        pwd_to_change = pwd_to_change or self.pwd
        pwds = []
        dates = self.generate_dates()

        for d in dates:
            pwds.append(str(d) + pwd_to_change)
            pwds.append(pwd_to_change + str(d))

        return pwds


class TitlecaseChanger(RuleGenerator):

    flag = "-t"

    def __init__(self, pwd):
        self.pwd = pwd

    def description(self):
        return ("""
        -t      This capitalizes the first character if it is a letter.
        """)

    def mutate(self, pwd_to_change=None):
        pwd_to_change = pwd_to_change or self.pwd
        pwds = []
        pwds.append(pwd_to_change.title())
        return (pwds)


class CaseInverter(RuleGenerator):

    flag = "-i"

    def __init__(self, pwd):
        self.pwd = pwd

    def description(self):

        return ("""
        -i      This inverts the case of the string.
        """)

    def mutate(self, pwd_to_change=None):

        pwd_to_change = pwd_to_change or self.pwd
        pwds = []
        pwds.append(pwd_to_change.swapcase())
        return (pwds)


class WordUpcaserDowncaser(RuleGenerator):

    flag = "-w"

    def __init__(self, pwd):
        self.pwd = pwd

    def description(self):
        return ("""
        -w      This upcases and downcases the entire string.
        """)

    def mutate(self, pwd_to_change=None):
        pwd_to_change = pwd_to_change or self.pwd
        pwds = []
        pwds.append(pwd_to_change.upper())
        pwds.append(pwd_to_change.lower())
        return (pwds)


class VowelsToNumbersChanger(RuleGenerator):

    flag = "-v"

    char_map = {
        'a': '4',
        'e': '3',
        'i': '1',
        'o': '0',
    }

    def description(self):
        return ("""
        -v      This changes all vowels to coresponding numbers.
                It covers all combinations of original vowels and number equivalents.
        """)

    def change_function(self, char, change):
        if char in self.chars and change == "1":
            return self.char_map[char.lower()]
        else:
            return char


class SymbolChanger(RuleGenerator):

    flag = "-x"

    char_map = {
        '+': '&',
        '&': '+',
        '!': '?',
        '?': '!',
    }

    def description(self):
        return ("""
        -x      This changes +/& !/? back and forth to explore other combinations
                It covers all combinations.
        """)

    def change_function(self, char, change):
        if char in self.chars and change == "1":
            return self.char_map[char]
        else:
            return char


class PopularSuffixAdder(RuleGenerator):

    flag = "-e"

    popular_suffixes = [
        '!',
        '?',
        '13',
        '7',
        '69',
        '23',
        '666',
        '777',
        '.',
    ]

    def description(self):
        return ("""
        -e      This adds popular suffixes to the password.
        """)

    def __init__(self, pwd):
        self.pwd = pwd

    def mutate(self, pwd_to_change=None):
        pwd_to_change = pwd_to_change or self.pwd
        pwds = []
        for suf in self.popular_suffixes:
            pwds.append(f"{pwd_to_change}{suf}")

        return (pwds)


class AToSymbolsChanger(RuleGenerator):

    flag = "-a"

    def description(self):
        return ("""
        -a      This changes all a and A characters to @ and & characters.
                It is done separately. If you want them to be mixed in with each other,
                you can use the -m flag with it. Example: -am
                It covers all combinations of a/A and @/&.
        """)

    def change_function(self, char, change):
        if char in self.chars and change == "1":
            return "@"
        else:
            return char

    def change_function2(self, char, change):
        if char in self.chars and change == "1":
            return "&"
        else:
            return char

    def mutate(self, pwd_to_change=None):
        pwd_to_change = pwd_to_change or self.pwd
        pwds = utilities.set_up_and_Change_characters(self.chars,
                                                      pwd_to_change,
                                                      self.change_function)
        pwds2 = utilities.set_up_and_Change_characters(self.chars,
                                                       pwd_to_change,
                                                       self.change_function2)
        return (pwds + pwds2)


class SToDollarSignChanger(RuleGenerator):

    flag = "-s"

    def description(self):
        return ("""
        -s      This changes out all s and S characters with dollar signs
                It covers all combinations of original s/S and $
        """)


class IToExclamationPointChanger(RuleGenerator):

    flag = "-h"

    def description(self):
        return ("""
        -h      This changes out all i and I characters with exclamation points
                It covers all combinations of original i/I and !
        """)


class CapitalLetterIntroducer(RuleGenerator):

    flag = "-z"

    def __init__(self, pwd):
        self.pwd = pwd

    def description(self):
        return ("""
        -z      !!!WARNING!!! This generates A LOT of noise.
                This changes lowercase letters to capital letters.
                It covers all combinations of lowercase and capital letters.
                It only affects letters that were original lowercase.
        """)

    def mutate(self, pwd_to_change=None):

        # Eventually change this function to use the set_up_and_change_characters function

        pwd_to_change = pwd_to_change or self.pwd
        pwds = []
        pwd_len = len(pwd_to_change)
        high_end_of_range = 2**(pwd_len) - 1
        for b in utilities.generate(high_end_of_range, len(pwd_to_change)):
            # can change this to the change_characters function
            pwds.append(
                utilities.transform_binary_into_capitals(b, pwd_to_change))

        # change this - using set to remove duplicates for right now
        return set(pwds)
