import utilities


class BaseWordChanger:
    def __init__(self, components):
        self.components = components

    def generate_word_variants(self):
        pwd_components_list = []
        pwd_components_list += utilities.set_up_and_change_words(
            self.components, self.word_change_function)
        return pwd_components_list


class WordUpcaserDowncaser(BaseWordChanger):
    def word_change_function1(self, word, value):
        if value == "1":
            return word.upper()
        else:
            return word

    def word_change_function2(self, word, value):
        if value == "1":
            return word.lower()
        else:
            return word

    def generate_word_variants(self):
        pwd_components_list = []
        pwd_components_list += utilities.set_up_and_change_words(
            self.components, self.word_change_function1)
        pwd_components_list += utilities.set_up_and_change_words(
            self.components, self.word_change_function2)
        return pwd_components_list


class WordTitlecaseChanger(BaseWordChanger):
    def word_change_function(self, word, value):
        if value == "1":
            return word.title()
        else:
            return word


class WordCaseInverter(BaseWordChanger):
    def word_change_function(self, word, value):
        if value == "1":
            return word.swapcase()
        else:
            return word
