from collections import deque


# from itertools import permutations # look into this more
# Function to generate binary numbers between 1 and `n` using the
# deque data structure
# Turned this into a generator so you don't have to hold this in memory
def generate(n, fill):
    # create an empty queue and enqueue 1
    q = deque()
    q.append('1')

    # run `n` times
    for i in range(n):
        # remove the front element
        front = str(q.popleft())

        # append 0 and 1 to the front element of the queue and
        # enqueue both strings
        q.append(front + '0')
        q.append(front + '1')

        # print the front element
        # print(f'{front.zfill(fill)}')
        yield (front.zfill(fill))


def transform_binary_into_capitals(binary, password):
    new_password = ''
    for idx, char in enumerate(binary):
        if char == '0':
            new_password += password[idx]
        else:
            new_password += password[idx].upper()

    return new_password


def get_indices_of_chars(chars, pwd):
    indices = []
    for idx, c in enumerate(pwd):
        if c in chars:
            indices.append(idx)
    return indices


def change_characters(idx_list, binary_range, fill, pwd, change_function):
    pwds = []
    for b in generate(binary_range, fill):
        temp_pwd = pwd
        for idx, unit in enumerate(b):
            pwd_idx = idx_list[idx]
            temp_pwd = temp_pwd[:pwd_idx] + change_function(
                temp_pwd[pwd_idx], b[idx]) + temp_pwd[(pwd_idx + 1):]
        pwds.append(temp_pwd)

    return (pwds)


def get_binary_range_and_fill(chars):
    num = 2**len(chars)
    return (num - 1, len(chars))


def set_up_and_Change_characters(chars, pwd, change_function):
    chars_in_password = [c for c in pwd if c in chars]
    chars_indices = get_indices_of_chars(chars_in_password, pwd)
    b_range, fill = get_binary_range_and_fill(chars_in_password)
    pwds = change_characters(chars_indices, b_range, fill, pwd,
                             change_function)
    return pwds


def change_words(words, b_range, fill, change_function):
    pwd_components_list = []
    for b in generate(b_range, fill):
        temp_components = []
        for idx, value in enumerate(b):
            temp_components.append(change_function(words[idx], value))

        pwd_components_list.append(temp_components)
    return pwd_components_list


def set_up_and_change_words(words, change_function):
    b_range, fill = get_binary_range_and_fill(words)
    pwds = change_words(words, b_range, fill, change_function)
    return pwds


def create_transformers_dict(transformers_list, pwd):

    transformers_dict = {}

    for t in transformers_list:
        t_class = t[0]
        function_arguments = t[1:]
        function_arguments.append(pwd)
        transformers_dict[t_class.flag] = t_class(*function_arguments)

    return transformers_dict
