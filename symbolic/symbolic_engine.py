import ast
import numbers

#import z3 to check assertions and evaluate the pct when reaching a return stmt
from z3 import *

#import os to fork an evaluation at an if/else stmt
import os, sys


class SymbolicEngine:
    def __init__(self, function_name, program_ast):
        self.fnc = find_function(program_ast, function_name)
        self.program_ast = program_ast
    
    # TODO: implement symbolic execution
    # The return value is a list of tuples [(input#1, ret#1), ...]
    # where input is a dictionary specifying concrete value used as input, e.g. {'x': 1, 'y': 2}
    # and ret is expected return value of the function
    # Note: all returned inputs should explore different program paths
    def explore(self):
        # Generates default input
        #unnecessary but we need to feed the function FunctionEvaluator with imput

        input = generate_inputs(self.fnc, {})

        f = FunctionEvaluator(self.fnc, self.program_ast, input)
        input_to_ret = f.eval_symbolic()
        
        assertion_violations_to_input = {}
        
        return (static_values_to_ret, assertion_violations_to_input)

###############
# Interpreter #
###############

#do not change
def run_expr(expr, fnc):
    if type(expr) == ast.Tuple:
        r = []
        for el in expr.elts:
            r.append(run_expr(el, fnc))
        return tuple(r)
    
    if type(expr) == ast.Name:
        if expr.id == 'True':
            return 1
        elif expr.id == 'False':
            return 0
        return fnc.state[expr.id]
    
    if type(expr) == ast.Num:
        assert (isinstance(expr.n, numbers.Integral))
        return expr.n

    if type(expr) == ast.BinOp:
        if type(expr.op) == ast.Add:
            return run_expr(expr.left, fnc) + run_expr(expr.right, fnc)
        if type(expr.op) == ast.Sub:
            return run_expr(expr.left, fnc) - run_expr(expr.right, fnc)
        if type(expr.op) == ast.Mult:
            return run_expr(expr.left, fnc) * run_expr(expr.right, fnc)
        if type(expr.op) == ast.Div:
            return run_expr(expr.left, fnc) / run_expr(expr.right, fnc)
        if type(expr.op) == ast.Mod:
            return run_expr(expr.left, fnc) % run_expr(expr.right, fnc)
        if type(expr.op) == ast.Pow:
            return run_expr(expr.left, fnc) ** run_expr(expr.right, fnc)
        
        # Evaluate only with constants
        if type(expr.op) == ast.LShift and type(expr.left) == ast.Num and type(expr.right) == ast.Num:
            return run_expr(expr.left, fnc) << run_expr(expr.right, fnc)
        if type(expr.op) == ast.RShift and type(expr.left) == ast.Num and type(expr.right) == ast.Num:
            return run_expr(expr.left, fnc) >> run_expr(expr.right, fnc)

    if type(expr) == ast.UnaryOp:
        if type(expr.op) == ast.Not:
            return not run_expr(expr.operand, fnc)
            if type(expr.op) == ast.USub:
                return -run_expr(expr.operand, fnc)

    if type(expr) == ast.Compare:
        assert (len(expr.ops) == 1)  # Do not allow for x==y==0 syntax
        assert (len(expr.comparators) == 1)
        e1 = run_expr(expr.left, fnc)
        op = expr.ops[0]
        e2 = run_expr(expr.comparators[0], fnc)
        if type(op) == ast.Eq:
            return e1 == e2
        if type(op) == ast.NotEq:
            return e1 != e2
        if type(op) == ast.Gt:
            return e1 > e2
        if type(op) == ast.GtE:
            return e1 >= e2
        if type(op) == ast.Lt:
            return e1 < e2
        if type(op) == ast.LtE:
            return e1 <= e2

    if type(expr) == ast.BoolOp:
        if type(expr.op) == ast.And:
            r = True
            for v in expr.values:
                r = r and run_expr(v, fnc)
            return r
        if type(expr.op) == ast.Or:
            r = False
            for v in expr.values:
                r = r or run_expr(v, fnc)
            return r

    if type(expr) == ast.Call:
        f = find_function(fnc.ast_root, expr.func.id)
            
        inputs = {}
        assert (len(expr.args) == len(f.args.args))
        # Evaluates all function arguments
        for i in range(0, len(expr.args)):
            inputs[f.args.args[i].id] = run_expr(expr.args[i], fnc)
            
        fnc_eval = FunctionEvaluator(f, fnc.ast_root, inputs)
        return fnc_eval.eval()
        
    raise Exception('Unhandled expression: ' + ast.dump(expr))


#do not change
def run_stmt(stmt, fnc):
    if type(stmt) == ast.Return:
        fnc.returned = True
        fnc.return_val = run_expr(stmt.value, fnc)
        return
    
    if type(stmt) == ast.If:
        cond = run_expr(stmt.test, fnc)
        if cond:
            run_body(stmt.body, fnc)
        else:
            run_body(stmt.orelse, fnc)
        return
    
    if type(stmt) == ast.Assign:
        assert (len(stmt.targets) == 1)  # Disallow a=b=c syntax
        lhs = stmt.targets[0]
        rhs = run_expr(stmt.value, fnc)
        if type(lhs) == ast.Tuple:
            assert (type(rhs) == tuple)
            assert (len(rhs) == len(lhs.elts))
            for el_index in range(len(lhs.elts)):
                el = lhs.elts[el_index]
                assert (type(el) == ast.Name)
                fnc.state[el.id] = rhs[el_index]
            return
        if type(lhs) == ast.Name:
            fnc.state[lhs.id] = rhs
            return

    if type(stmt) == ast.Assert:
        #nothing to do here, only assert when in symbolic
        return
        
        raise Exception('Unhandled statement: ' + ast.dump(stmt))

#new
def eval_stmt(stmt, fnc):
    if type(stmt) == ast.Return:
        fnc.returned = True
        fnc.return_val = run_expr(stmt.value, fnc)

        #add the symbolic values in symbolic_dict to the pct
        for key in fnc.symbolic_dict:
            print key + " == " + fnc.symbolic_dict[key]
            #see if it's not trivial
            if key != fnc.symbolic_dict[key]:
                print "Its not trivial" #debug
               # fnc.pct.add(key + " == " + fnc.symbolic_dict[key])
            else:
                print "Its trivial" #debug
                #if it can be anything, set it to 0
                #TODO: make sure, dummy_variable is not used in the input program
                temp = Int(str(key))
                dummy_variable = Int('dummy_variable' + str(key))
                fnc.pct.add(temp == dummy_variable)
                fnc.pct.add(dummy_variable == temp)
                print fnc.pct


        if (fnc.pct.check() == sat):
            print ("Found a satisfiable stmt")
            sat_model = fnc.pct.model()
            print sat_model
            sat_dict = model_to_dictionary(sat_model)
            fnc.values_to_ret.append((sat_dict, fnc.return_val)) #does not work, its local

            #TODO: acquire lock
            static_values_to_ret.append((sat_dict, fnc.return_val))
            #TODO: release lock
        return
    
    if type(stmt) == ast.If:
        cond = run_expr(stmt.test, fnc)

        #fork to evaluate both if and else bodies
        pid = os.fork()
        if (pid == 0):
            #child
            print ("A child was born")
            fnc.parent = False

            #TODO: add the stmt.test to the fnc.pct in the right FORMAT
            #fnc.pct.add(stmt.test)
            eval_body(stmt.body, fnc)

        else:
            #parent
            print("I became a parent")
            
            #TODO: add the negation of stmt.test to the fnc.pct in the right FORMAT
            #fnc.pct.add(Not(stmt.test))
            eval_body(stmt.orelse, fnc)
            #TODO: wait for child
            os.waitpid(pid,0)
        return
    
    # lots TODO here
    if type(stmt) == ast.Assign:
        assert (len(stmt.targets) == 1)  # Disallow a=b=c syntax
        lhs = stmt.targets[0]
        #print stmt.targets[0] #debug
        rhs = run_expr(stmt.value, fnc)
        if type(lhs) == ast.Tuple:
            assert (type(rhs) == tuple)
            assert (len(rhs) == len(lhs.elts))
            for el_index in range(len(lhs.elts)):
                el = lhs.elts[el_index]
                assert (type(el) == ast.Name)
                fnc.state[el.id] = rhs[el_index]
            return
        if type(lhs) == ast.Name:
            fnc.state[lhs.id] = rhs
            return

    if type(stmt) == ast.Assert:
        # TODO: implement check whether the assertion holds.
        # However do not throw exception in case the assertion does not hold.
        # Instead return inputs that trigger the violation from SymbolicEngine.explore()
        return
        
    raise Exception('Unhandled statement: ' + ast.dump(stmt))


#do not change
def run_body(body, fnc):
    for stmt in body:
        run_stmt(stmt, fnc)
        if fnc.returned:
            return

#new
def eval_body(body, fnc):
    for stmt in body:
        eval_stmt(stmt, fnc)
        if fnc.returned:
            #kill process if it's a child
            if fnc.parent == False:
                sys.exit()
            #TODO: delete the dummy_variables from the output 
            #else :
                
            return


class FunctionEvaluator:
    def __init__(self, f, ast_root, inputs):
        assert (type(f) == ast.FunctionDef)
        for arg in f.args.args:
            assert arg.id in inputs
        
        self.state = inputs.copy()
        self.returned = False
        self.return_val = None
        self.ast_root = ast_root
        self.f = f

        #new
        self.pct = Solver()
        self.values_to_ret = []

        #make symbolic dictonary that has as key 'x' and as value '3' or '5/5 + y'
        self.symbolic_dict = {}

        for i in range(0, len(f.args.args)):
            self.symbolic_dict[f.args.args[i].id] = str(f.args.args[i].id)

        print "Symbolic dictionary:", 
        print self.symbolic_dict #debug

        #only the parent of all processes is allowed to return
        self.parent = True
    
    def eval(self):
        run_body(self.f.body, self)
        
        assert (self.returned)
        return self.return_val

    def eval_symbolic(self):
        eval_body(self.f.body, self)
        
        assert (self.returned)
        return self.values_to_ret

#TODO: make it thread-safe
static_values_to_ret = []

####################
# Helper Functions #
####################

# f: function for which to generate inputs
# inputs: dictionary that maps argument names to values. e.g. {'x': 42 }
def generate_inputs(f, inputs):
    inputs = {}
    for arg in f.args.args:
        assert (type(arg) == ast.Name)
        if arg.id in inputs:
            inputs[arg.id] = inputs[arg.id]
        else:
            # By default input are set to zero
            inputs[arg.id] = 0
    return inputs


def find_function(p, function_name):
    assert (type(p) == ast.Module)
    for x in p.body:
        if type(x) == ast.FunctionDef and x.name == function_name:
            return x
    raise LookupError('Function %s not found' % function_name)

#new
def model_to_dictionary(model):
    stmts = str(model).split(",")
    for stmt in stmts:
        #TODO: fix this, right now it doesn't delete the characters
        stmt = "".join([char for char in stmt if (char not in [' ', '[', ']'])])
    return {k:v for k,v in (x.split('=') for x in stmts) }


