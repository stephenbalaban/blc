#!/usr/bin/env python
"""
    test_blc.py
    ~~~~~~~~~~~

    Test our BLC parser/interpreter

    :created: 2019-12-21 19:03:17 -0800
    :license: All Rights Reserved.
"""
import blc
from blc import LAMBDA


def passert_eq(raw_str, expectation):
    # Use id for name
    parsed = blc.parse_raw(raw_str)
    msg = ("{} test: '{}' => '{}' expected but got '{}'"
           .format('parse', raw_str, expectation, parsed))
    assert parsed == expectation, msg
    print("{} passed {} test r={}".format(raw_str, 'parse', expectation))


def nassert_eq(raw_str, expectation):
    assert_eq(raw_str, blc.is_normal_form, expectation)


def rassert_eq(raw_str, expectation):
    assert_eq(raw_str, blc.evaluate, expectation)


def assert_eq(raw_str, fn, expectation):
    # Normal form tests
    parsed = blc.parse_raw(raw_str)
    result = fn(parsed)
    msg = ("{} test: ({}) '{}' => '{}' expected but got '{}'"
           .format(fn.__name__, raw_str, parsed, expectation, result))
    assert result == expectation, msg
    print("{} ({}) passed {} test {}".format(raw_str, parsed, fn.__name__,
                                             expectation))


def sassert_eq(lhs, rhs, expectation):
    # Substitution tests.
    result = blc.substitute(lhs, rhs)
    msg = ("substitution test: ('{}', '{}') => '{}' expected but got '{}'"
           .format(lhs, rhs, expectation, result))
    assert result == expectation, msg
    print("{}/{} passed substitution test {}"
          .format(lhs, rhs, result))


if __name__ == '__main__':
    # parse
    # invalid
    passert_eq('000100011100110100001110011010',
               (LAMBDA, [(LAMBDA, [1, [0, 0]]), (LAMBDA, [1, [0, 0]])]))
    passert_eq('001110', (LAMBDA, 2))
    passert_eq('00110', (LAMBDA, 1))
    passert_eq('0010', (LAMBDA, 0))
    passert_eq('010001101000011010', [(LAMBDA, [0, 0]), (LAMBDA, [0, 0])])
    passert_eq('00011010', (LAMBDA, [0, 0]))
    passert_eq('0100100010', [(LAMBDA, 0), (LAMBDA, 0)])
    passert_eq('01000110100010', [(LAMBDA, [0, 0]), (LAMBDA, 0)])
    passert_eq('010000000101111010011101000011010',
               [(LAMBDA, (LAMBDA, (LAMBDA, [[2, 0], [1, 0]]))),
                (LAMBDA, [0, 0])])

    # normal check
    nassert_eq('0010', True)
    nassert_eq('00011010', True)
    nassert_eq('0100100010', False)
    nassert_eq('00000100100010', False)
    nassert_eq('0101000010001000111110', False)

    # substitution check (before dropping head)
    sassert_eq((LAMBDA, 0), (LAMBDA, 4), (LAMBDA, 4))

    # shift free variables in rhs
    sassert_eq((LAMBDA, (LAMBDA, [0, 1])), (LAMBDA, 5),
               (LAMBDA, [0, (LAMBDA, 6)]))

    # decrement free variables in lhs
    pass

    # shifting only free variables
    sassert_eq((LAMBDA, (LAMBDA, [[0, 2], 1])), (LAMBDA, [[7, 0], 1]),
               (LAMBDA, [[0, 1], (LAMBDA, [[8, 0], 2])]))

    # (λ λ 3 1 (λ 0 2)) (λ 4 0)
    # λ ((2 (λ 5 0)) (λ 0 (λ 6 0)))
    sassert_eq((LAMBDA, (LAMBDA, [[3, 1],
                                  (LAMBDA, [0, 2])])),
               (LAMBDA, [4, 0]),
               (LAMBDA, [[2, (LAMBDA, [5, 0])],
                         (LAMBDA, [0, (LAMBDA, [6, 0])])]))

    a = (LAMBDA, (LAMBDA, (LAMBDA, [2, 1])))
    b = (LAMBDA, (LAMBDA, (LAMBDA, [[1, 0], 2])))
    r = (LAMBDA, (LAMBDA, [(LAMBDA, (LAMBDA, (LAMBDA, [[1, 0], 2]))), 1]))
    sassert_eq(a, b, r)

    # evaluation tests
    rassert_eq('010000000111101100000000101110101110',
               (LAMBDA, (LAMBDA, (LAMBDA, (LAMBDA, [[1, 0], 3])))))
    rassert_eq('0101000010001000111110', (LAMBDA, 4))
    rassert_eq('01000110100010', (LAMBDA, 0))
    rassert_eq('010001101000000101101010', (LAMBDA, [[0, 0], 0]))
    # first
    rassert_eq('0101000010001000111110', (LAMBDA, 4))
    # second
    rassert_eq('01010000110001111000111110', (LAMBDA, 3))

    # Pow 0^2
    rassert_eq('010000011100111010000010',
               (LAMBDA, (LAMBDA, 0)))

    # Pow 1^1
    rassert_eq('010000011101000000111010',
               (LAMBDA, (LAMBDA, [1, 0])))

    # Pow 1^3
    rassert_eq('0100000111001110011101000000111010',
               (LAMBDA, (LAMBDA, [1, 0])))

    # Pow 2^1
    rassert_eq('01000001110100000011100111010',
               (LAMBDA, (LAMBDA, [1, [1, 0]])))

    # Pow 2^2
    rassert_eq('0100000111001110100000011100111010',
               (LAMBDA, (LAMBDA, [1, [1, [1, [1, 0]]]])))

    # Pow 3^2
    rassert_eq('010000011100111010000001110011100111010',
               (LAMBDA, (LAMBDA,
                [1, [1, [1, [1, [1, [1, [1, [1, [1, 0]]]]]]]]])))

    # Pow 2^3
    rassert_eq('010000011100111001110100000011100111010',
               (LAMBDA, (LAMBDA, [1, [1, [1, [1, [1, [1, [1, [1, 0]]]]]]]])))
