#!/usr/bin/python

import ast
import sys
import platform

from symbolic import SymbolicEngine, find_function, FunctionEvaluator, generate_inputs

import types
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def run_app(program):
    program_ast = ast.parse(program)
    fnc = find_function(program_ast, 'main')
    inputs = generate_inputs(fnc, {})
    f = FunctionEvaluator(fnc, program_ast, inputs)
    ret = f.eval()
    print("Executed function 'main' with inputs '%s' and result '%s'" % (str(inputs), str(ret)))


def eval_app(program):
    program_ast = ast.parse(program)

    engine = SymbolicEngine('main', program_ast)
    (input_to_ret, violated_assertion_to_input) = engine.explore()

    # input_to_ret is a dictionary from inputs to return values
    assert (isinstance(input_to_ret, list))
    for (input, ret) in input_to_ret:
        # The inputs are dictionary from variable names to their values, e.g., {'x': 1, 'y': 0}
        assert(isinstance(input, dict))
        # The return value is expected to be integer
        assert(isinstance(ret, int))

    # violated_assertion_to_input is a dictionary from violated assertion to inputs
    for key, val in violated_assertion_to_input.iteritems():
        assert (isinstance(key, ast.Assert))
        assert (isinstance(val, dict))

    print("Violated Assertions: " + str(violated_assertion_to_input))
    print("Execution Path Inputs: " + str(input_to_ret))

    try:
        oracle = find_function(program_ast, 'expected_result')
        assert (len(oracle.body) == 1)
        assert (type(oracle.body[0]) == ast.Return)
        assert (type(oracle.body[0].value) == ast.List)
        expected = set()
        for expr in oracle.body[0].value.elts:
            expected.add(expr.n)

        return_values = set([ret for input,ret in input_to_ret])
        if expected == return_values:
            print ('Returned values as expected.')
            sys.exit(0)
        else:
            print ('Returned values do not match expected return values!')
            print ('Expected: ' + str(expected))
            print ('Actual: ' + str(return_values))
            sys.exit(1)
    except LookupError:
        pass


def print_usage():
    usage = """
Usage:
    # Option run executes main function with arguments initialized to 0
    %(cmd)s run <python_file>
    # Option eval executes main function symbolically
    %(cmd)s eval <python_file>
            """ % {"cmd": sys.argv[0]}
    print(usage)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage()
        exit(1)

    if platform.python_version() != '2.7.6':
        print("Warning: expected python version '2.7.6'.")

    if sys.argv[1] == 'eval':
        eval_app(open(sys.argv[2], 'rt').read())
    elif sys.argv[1] == 'run':
        run_app(open(sys.argv[2], 'rt').read())
    else:
        print("Unknown command %s" % (sys.argv[1]))
        print_usage()
        exit(1)