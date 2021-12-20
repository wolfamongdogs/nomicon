# NOMICON

**DISCLAIMER: This tool is not to be used illegaly or to violate anyone's privacy. It is a tool for pentesting and specifically checking the integrity of passwords.**

I put together this tool to generate password lists to be used with different brute-forcing tools (Hydra, John The Ripper, etc.). There are many great wordlists already available, but consider the following scenarios. 

1. The wordlists you have tried haven't worked. You have a known password of the target but it no longer works. People are generally bad at remembering highly varied passwords, so you can use the transform and/or generate function in a couple ways to generate variations on that password that you can use. Many people change the letter "A" to "@" or add an "!" or various other typical transformations. 

2. You know information about a target and want to create passwords from this information. For instance, you know their pet's name, anniversary date, favorite band, etc. You can feed this information into NOMICON and generate a bunch of different passwords with every combination of these and various capitalization and concatenation options.

Passwords will be output into files named after thier components, the flags you executed the script with, and the number of results. 

Also, the passwords will be sorted by either levenshtein distance or length. If you are mutating a single password, output will be sorted by levenshtein distance, if you are generating passwords out of components, output will be sorted by length.

## 1. Generating passwords from password components.

If you run it with something like:

```python3 main.py -g foo bar baz bleurgh blast```

It will give you back all permutations from one word to the length of the arguments.
It will also add in case inversion, all caps, and title case for each portion. You will also get every combination possible with those as well.

Check out the output in ```examples/foo-bar-baz-bleurgh-blast_g_12335.txt``` 

## 2. Transforming passwords.

If you run it with something like:

```python3 main.py -saved password```

It will give you back the password ('password' in this case) with the following changes:

1. It will transform the letter "a/A" to "@" and "&".
2. It will transform the letter "s/S" to "$".
3. It will also transform vowels into their number counterparts.
4. It will add popular endings to the password as defined in the ```rules.py``` file.
5. It will add the current date (and the previous 5 years) to the end and beginning of the password.

Check out the output in ```exapmles/password_saved_29.txt```

It does all of these separately and it generated 29 passwords. To start mixing these together you can add the ```-m``` flag as many times as necessary. 

```python3 main.py -msaved password```

Check out the output in ```examples/password_msaved_564.txt```

You now get two levels of mixing based on the previous passwords transformed. So you went from 29 passwords to 564 passwords generated. Some passwords are very more likely than others. For example ```pa$$word?``` vs. ```password20192019```

You can also mix again by adding an additional ```-m``` flag.

```python3 main.py -mmsaved password```

Checkout the output in ```examples/password_mmsaved_1021.txt```

You now get 3 levels of mixing and 1,021 passwords.

Again, some passwords are much more likely to be helpful than others ```p4$$word!``` vs. ```2017pa$$word2016```

## 3. Doing both 1 & 2 at the same time.

If you run it with something like:

```python3 main.py -gasv foo bar baz```

Check out the output in ```examples/foo-bar-baz_gasv_2436.txt```

You will generate passwords with the components "foo", "bar", and "baz".
You will also then mutate all of those passwords with the "-a", "-s", and "-v" flags described above. 

# Options

```python3 main.py``` run without any parameters or arguments will show you usage information.

```
        Welcome to Mutator v.1.0!
        Take a known password and transform it using common methods.
        python3 main.py [-mcaves] [password]

        Options
        

        -v      This changes all vowels to coresponding numbers.
                It covers all combinations of original vowels and number equivalents.
        

        -e      This adds popular suffixes to the password.
        

        -a      This changes all a and A characters to @ and & characters.
                It is done separately. If you want them to be mixed in with each other,
                you can use the -m flag with it. Example: -am
                It covers all combinations of a/A and @/&.
        

        -s      This changes out all s and S characters with dollar signs
                It covers all combinationso f original s/S and $
        

        -z      !!!WARNING!!! This generates A LOT of noise.
                This changes lowercase letters to capital letters.
                It covers all combinations of lowercase and capital letters.
                It only affects letters that were original lowercase.
        

        -d      This adds the current date as well as 5 years previous
                to the front and back of the password.
        

        -x      This changes +/& !/? back and forth to explore other combinations
                It covers all combinations.
        

        -t      This capitalizes the first character if it is a letter.
        

        -w      This upcases and downcases the entire string.
        

        -i      This inverts the case of the string.
        

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
```

# More Exmaples.

All of these can be found in the examples so you can see how they work.

This will limit the permutations to lengths of 3 components. 1,055 passwords generated.
```python3 main.py -gq 3 foo bar baz bleurgh blast```


This will use all permutations from 1 up to all 5 components. 12,335 passwords generated.
```python3 main.py -g foo bar baz bleurgh blast```

Experiment with the options and see which ones work best for you. Try mixing several times. And be aware that the size can grow exponentially depending on the components, password, and options. For example:

```python3 main.py -gsaved foo bar baz bleurgh blast```
This ran for several minutes and produced 1,019,028 passwords.

So it is highly recommended when running ```-g``` with a lot of password componentes using ```-q``` to limit the permutations. 3 is a good number to use.


