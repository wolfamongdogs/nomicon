# NOMICON

This tool can be used for several things.

## 1. Generating passwords from password components.

If you run it with something like:

```python3 main.py -g foo bar baz bleurgh blast```

It will give you back all permutations from one wrod to the length of the arguments.
It will also add in case inversion, all caps, and title case for each portion. You will also get every combination possible with those as well.

## 2. You can transform a password.

If you run it with something like:

```python3 main.py -asv password```

It will give you back the password ('password' in this case) with the following changes:

1. It will transform the letter "a/A" to "@" and "&".
2. It will transform the letter "s/S" to "$".
3. It will also transform vowels into their number counterparts.

## 3. You can do both of the above

If you run it with something like:

```python3 main.py -gasv foo bar baz```

You will generate passwords with the components "foo", "bar", and "baz".
You will also then mutate all of those passwords with the same transformations above.

More documentation to come...

