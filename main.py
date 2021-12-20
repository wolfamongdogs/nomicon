import sys
from Levenshtein import distance as lev
import getopt
import itertools
from transformers import transformers
import utilities
from word_component_mangler import WordCaseInverter, WordTitlecaseChanger, WordUpcaserDowncaser

# TODO: Add warning if the user uses -g with over 8 options. Maybe even add an "are you sure?"
# TODO: LOW PRIORITY - expand generator to do more than base 2


class Arguments:
    def __init__(self, argv):
        self.optlist, self.args = getopt.getopt(
            argv,
            self.extract_flags_from_clsses(transformers) + 'mgcq:')

        self.options_passed = [o[0] for o in self.optlist]
        self.password = ''.join(self.args)

        if "-q" in self.options_passed:
            # You can set a quality for the g flag to change how many permutations you do
            # Without the g flag it won't do anything
            self.quality = int([o[1] for o in self.optlist if o[0] == "-q"][0])
        else:
            self.quality = len(self.args)

    # This just pulls the flags passed in so you can see what's there
    def extract_flags_from_clsses(self, transformers_list):
        flags = ""
        for t in transformers_list:
            flags += t[0].flag.replace("-", "")

        return flags


class Mutator(Arguments):
    def __init__(self, argv):

        super().__init__(argv)
        self.final_passwords = []
        self.transformers = utilities.create_transformers_dict(
            transformers, self.password)
        if len(self.optlist) == 0:
            self.help()

    def levenshtein_sort_function(self, s):
        return lev(s, self.password)

    def help(self):
        print("""
        Welcome to Mutator v.1.0!
        Take a known password and transform it using common methods.
        python3 main.py [-mcaves] [password]

        Options
        """)

        for t in self.transformers:
            print(self.transformers[t].description())

        print("""
        -m      This mutates again with the same options to get more combinations.
                You can add multiple m's to keep mutating (-mm or -mmm)

        -g      This allows you to generate passwords based on components.
                This can be portions of a password that stick out as separate things.
                It can also be important information about the target.

        -q      This can be used with -g to limit the permutations of password components.
                For example "-gq 3 foo bar baz bleurgh blast" would return passwords generated
                with those components but only go up to combinations of 3, whereas leaving off
                "-q 3" would go up to permutations that are all 5 components long.

      Examples:
      python3 main.py -mcaves password
      python3 main.py -g part1 part2 part3
      python3 main.py -gq 3 foo bar baz blargh blam bling
      """)

    def mutate(self, pwd=None):
        pwds = []
        for opt in self.options_passed:
            if opt != "-m" and opt != "-g" and opt != "-c" and opt != "-q":
                #clunky way of removing dupes
                pwds += list(set(self.transformers[opt].mutate(pwd)))

        self.final_passwords += pwds

        if "-m" in self.options_passed:
            self.options_passed.remove('-m')
            for pw in pwds:
                self.mutate(pw)

    def show_final_passwords(self):
        # Find a better way to eliminate redundancy than casting to a set
        return (list(set(self.final_passwords)))


# This class is responsible for generating all permutations of the included password components.
# It also includes a couple different ways of combining the passwords
class PWGenerator(Arguments):
    def __init__(self, argv):
        super().__init__(argv)
        self.passwords = self.args

    def generate_permutations(self):
        perms = []
        proc_perms = []

        for idx in range(self.quality):
            temp = itertools.permutations(self.passwords, idx + 1)
            perms += temp

        for p in perms:
            proc_perms += WordCaseInverter(p).generate_word_variants()
            proc_perms += WordTitlecaseChanger(p).generate_word_variants()
            proc_perms += WordUpcaserDowncaser(p).generate_word_variants()

        proc_perms += perms
        return proc_perms

    def join_perms(self, perms):
        pwds = []
        for p in perms:
            pwds.append("".join(p))
            if "-c" in self.options_passed:
                pwds.append("+".join(p))
                pwds.append("&".join(p))

        # Clunky way of getting rid of duplicates
        return list(set(pwds))

    def gimme_passwords(self):
        pwds = self.join_perms(self.generate_permutations())
        return pwds


# This is the output section.


def final_passwords_stats(final_pwds, options_passed):
    print(
        f"Mutator v.1.1 was run with the following arguments: {options_passed}"
    )
    print(f"You have generated {len(final_pwds)} passwords.")
    if ('-g' in options_passed and len(options_passed) > 1):
        print('Sorted by password length.')
    else:
        print('Sorted by Levenshtein distance.')


# This is the main function called when invoking this.
# It is responsible for spawning all the classes etc.
def mutate(argv):
    loader_index = 0
    loader_list = ['|||||', '/////', '-----', '\\\\\\\\\\']
    args = Arguments(argv)
    final_pwds = []
    if ('-g' in args.options_passed and len(args.args) > 5
            and len(args.options_passed) > 4):
        print("==================================")
        print("Buckle up this could take a while!")
        print("==================================")
    else:
        print("===================================")
        print("Generating passwords beep beep boop")
        print("===================================")

    if "-g" in args.options_passed:
        gen = PWGenerator(argv)
        pwds = gen.gimme_passwords()
        final_pwds += pwds
        if len(args.options_passed) > 1:
            for p in pwds:
                print(loader_list[loader_index], end='\r')
                loader_index = (loader_index + 1) % len(loader_list)
                m = Mutator(argv)
                m.mutate(p)
                final_pwds += m.show_final_passwords()
                final_pwds.sort(key=len)
    else:
        m = Mutator(argv)
        m.mutate()
        final_pwds += m.show_final_passwords()
        final_pwds.sort(key=m.levenshtein_sort_function)

    filename = f"{'-'.join(args.args)}_{''.join(args.options_passed).replace('-','')}_{len(final_pwds)}.txt"
    with open(filename, 'w') as f:
        for p in final_pwds:
            f.write(f"{p}\n")
        print(f"{filename} created.")
    final_passwords_stats(final_pwds, args.options_passed)


if __name__ == "__main__":
    mutate(sys.argv[1:])
