#!/usr/bin/env python
"""
    A BLC parser/interpreter in python

    :created: 2019-12-14 12:35:36 -0800
    :copyright: (c) 2019, Stephen A. Balaban
    :license: MIT
"""
import sys


def getc():
    return sys.stdin.read(1)


# Non-terminals
NT_LAMBDA = '00'
NT_APPLY = '01'


def IS_VAR(two):
    return two == '10' or two == '11'


# Terminals
LAMBDA = 'λ'
APPLY = 'A'

# Grammar
# 1^{n+1}0  = int
# 00M       = (LAMBDA, M)
# 01MN      = [M, N]


def lex(source_string):
    L = NT_LAMBDA
    A = NT_APPLY

    i = 0
    while True:
        try:
            two = source_string[i] + source_string[i + 1]
        except IndexError:
            break
        if two == L:
            i = i + 2
            yield LAMBDA
        elif two == A:
            i = i + 2
            yield APPLY
        elif IS_VAR(two):
            n = source_string[i + 1]
            msg = "Must be either 0, 1. Got = '" + n + "'"
            assert n == '0' or n == '1', msg
            dbindex = 0
            while n != '0':
                dbindex += 1
                n = source_string[i + 1 + dbindex]
            i = i + 2 + dbindex
            yield dbindex
        else:
            assert False, "Not a valid character."


def body(expr):
    """Gets the body of a parsed lambda (represented as 2-tuples)"""
    assert type(expr) == tuple
    return expr[1]


def end_of_first_lambda(a):
    for index in range(len(a)):
        c = a[index]
        cn = a[index + 1]
        if type(c) == int and (cn == LAMBDA or cn == APPLY):
            return index + 1


def find_argument(a):
    """
    start of first lambda or free variable reading right (this is the b portion
    of an (a b) application).
    """
    if len(a) == 3:
        x, y, z = a
        if x == APPLY and type(y) == int and type(z) == int:
            return 2
    for index in reversed(range(len(a))):
        c = a[index]
        cp = a[index - 1]
        if c == LAMBDA and type(cp) == int:
            return index
        if c == APPLY and type(cp) == int:
            return index
    assert False, "Couldn't find a lambda or variable, malformed code."


def parse(tokens):
    """
    Every time you generate a statement, backtrack to see if you have completed
    an application.
    """
    revlist = list(reversed(tokens))
    stack = []
    for tok in revlist:
        if type(tok) == int:
            r = parse_var(tok, stack)
        elif tok == APPLY:
            r = parse_apply(tok, stack)
        elif tok == LAMBDA:
            r = parse_lambda(tok, stack)
        else:
            assert False, "nope."
        stack.insert(0, r)
    return stack.pop(0)


def parse_lambda(tok, context):
    body = context.pop(0)
    return (LAMBDA, body)


def parse_apply(tok, context):
    lhs = context.pop(0)
    rhs = context.pop(0)
    return [lhs, rhs]


def parse_var(tok, context):
    return tok


def read():
    raw_text = ''.join(sys.stdin)
    print("raw text: " + raw_text)
    return parse_raw(raw_text)


def parse_raw(raw_text):
    return parse(list(lex(raw_text)))


def pprint(parse_tree):
    print(parse_tree)


def beta_reduce(tree, verbose=False):
    return tree


def is_head_normal_form(parse_tree):
    return type(parse_tree) != list


def evaluate(parse_tree, verbose=True):
    idx = 0
    while is_head_normal_form(parse_tree):
        redex = beta_reduce(parse_tree, verbose=verbose)
        if verbose:
            print("{}   {} => {}".format(idx, parse_tree, redex))
        parse_tree = redex
        idx += 1
    if verbose:
        print("{}   {}".format(idx, parse_tree))
    return parse_tree


def is_normal_form(tree, verbose=True):
    if type(tree) == list:
        if type(tree[0]) == tuple:
            return False
        else:
            return is_normal_form(tree[0]) and is_normal_form(tree[1])
    elif type(tree) == tuple:
        return is_normal_form(tree[1])
    elif type(tree) == int:
        return True
    else:
        raise Exception("Unknown type.")


if __name__ == '__main__':
    pprint(evaluate(read()))
