import ast
import numbers
import copy

#import z3 to check assertions and evaluate the pct when reaching a return stmt
from z3 import *

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

        print input_to_ret #debug
        assertion_violations_to_input = {}
        
        #right now, input_to_ret has dictionaries where there value is in string format
        #that's why this throws an exception, because it expects an int
        return (input_to_ret, assertion_violations_to_input)

###############
# Interpreter #
###############


#new
# turn everything into a string, such that the expression is not run
def eval_expr(expr, fnc, negate):
    if type(expr) == ast.Tuple:
        r = []
        for el in expr.elts:
            r.append(eval_expr(el, fnc, False))
        return tuple(r)
    
    if type(expr) == ast.Name:
        if expr.id == 'True':
            if negate:
                return 0
            else: 
                return 1
        elif expr.id == 'False':
            if negate:
                return 1
            else: 
                return 0
        #does this work? if so, it would be brilliant
        return Int(fnc.symbolic_dict[expr.id])
    
    if type(expr) == ast.Num:
        assert (isinstance(expr.n, numbers.Integral))
        return expr.n

    #additionaly, we need brackets
    if type(expr) == ast.BinOp:
        if type(expr.op) == ast.Add:
            return Sum( eval_expr(expr.left, fnc, negate), eval_expr(expr.right, fnc, negate) )
        if type(expr.op) == ast.Sub:
            return  eval_expr(expr.left, fnc, negate) - eval_expr(expr.right, fnc, negate)
        if type(expr.op) == ast.Mult:
            return Product( eval_expr(expr.left, fnc, negate), eval_expr(expr.right, fnc, negate) )
        if type(expr.op) == ast.Div:
            return eval_expr(expr.left, fnc, negate) / eval_expr(expr.right, fnc, negate)
        if type(expr.op) == ast.Mod:
            return eval_expr(expr.left, fnc, negate) % eval_expr(expr.right, fnc, negate)
        if type(expr.op) == ast.Pow:
            return eval_expr(expr.left, fnc, negate) ** eval_expr(expr.right, fnc, negate)
        
        # Evaluate only with constants
        if type(expr.op) == ast.LShift and type(expr.left) == ast.Num and type(expr.right) == ast.Num:
            return eval_expr(expr.left, fnc, negate) <<  eval_expr(expr.right, fnc, negate)
        if type(expr.op) == ast.RShift and type(expr.left) == ast.Num and type(expr.right) == ast.Num:
            return LShR(eval_expr(expr.left, fnc, negate),  eval_expr(expr.right, fnc, negate))


    if type(expr) == ast.UnaryOp:
        if type(expr.op) == ast.Not:
            if negate:
                return eval_expr(expr.operand, fnc, False)
            else:
                return Not( eval_expr(expr.operand, fnc, False))
           # if type(expr.op) == ast.USub:
            #    return - eval_expr(expr.operand, fnc) 

    if type(expr) == ast.Compare:
        assert (len(expr.ops) == 1)  # Do not allow for x==y==0 syntax
        assert (len(expr.comparators) == 1)
        e1 = eval_expr(expr.left, fnc, False)
        op = expr.ops[0]
        e2 = eval_expr(expr.comparators[0], fnc, False)
        if type(op) == ast.Eq:
            if negate:
                return e1 != e2
            else:
                return  e1 == e2 
        if type(op) == ast.NotEq:
            if negate:
                return e1 == e2
            else:
                return e1 != e2
        if type(op) == ast.Gt:
            if negate:
                return e1 <= e2
            else:
                return e1 > e2 
        if type(op) == ast.GtE:
            if negate:
                return e1 < e2
            else: 
                return e1 >= e2 
        if type(op) == ast.Lt:
            print "Evaluating", str(e1) +'<' + str(e2) #Debug
            if negate:
                return e1 >= e2
            else: 
                return e1 < e2 
        if type(op) == ast.LtE:
            if negate:
                return e1 > e2
            else: 
                return e1 <= e2 

    if type(expr) == ast.BoolOp:
        if type(expr.op) == ast.And:
            if negate:
                r = False
            else:
                r = True
            for v in expr.values:
                r = And(r, eval_expr(v, fnc, False) )
            return r
        if type(expr.op) == ast.Or:
            if negate:
                r = True
            else: 
                r = False
            for v in expr.values:
                r = Or (r ,eval_expr(v, fnc, False))
            return r

    #TODO:
    # check if the symbols used in the function call might interfere with this function
    # handle all the complifications of a function call
    # lots to do here!
    if type(expr) == ast.Call:
        f = find_function(fnc.ast_root, expr.func.id)
            
        inputs = {}
        assert (len(expr.args) == len(f.args.args))
        # Evaluates all function arguments
        for i in range(0, len(expr.args)):
            inputs[f.args.args[i].id] = run_expr(expr.args[i], fnc)
            
        fnc_eval = FunctionEvaluator(f, fnc.ast_root, inputs)
        #do this symbolically
        #TODO: lots to do here
        return fnc_eval.eval_symbolic()
        
    raise Exception('Unhandled expression: ' + ast.dump(expr))

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
        if fnc.parents_of_all_children:
            fnc.returned = True
        #should actually be eval_expr
        fnc.return_val = eval_expr(stmt.value, fnc, False)

        #add the symbolic values in symbolic_dict to the pct
        for key in fnc.symbolic_dict:
            #print key + " == " + fnc.symbolic_dict[key] #debug
            #see if it's not trivial
            if key != fnc.symbolic_dict[key]:
                #print "Its not trivial" #debug
                fnc.pct.add(Int(key) == fnc.symbolic_dict[key])

        if (fnc.pct.check() == sat):
            print ("Found a satisfiable stmt") #debug
            sat_model = fnc.pct.model()
            print sat_model #debug
            sat_dict = {}
            if sat_model: #see if it is not empty
                sat_dict = model_to_dictionary(sat_model)

            sat_dict = cleanup_dictionary_to_only_inputs(sat_dict, fnc)

            fnc.values_to_ret.append((sat_dict, fnc.return_val)) 
        else:
            print "This is not satisfiable"
    
        return
    
    if type(stmt) == ast.If:
        cond = eval_expr(stmt.test, fnc, False)
        print (cond)

        eval_expr_result = eval_expr(stmt.test, fnc, False)

        #save the pct
        save_pct = Solver()
        save_pct.assert_exprs(fnc.pct.assertions())

        #add it to the pct
        fnc.pct.add(eval_expr_result)

        #<DEBUG>:
        if (fnc.pct.check() == sat):
            print "Model of the if clause: ", fnc.pct.model()
        #</DEBUG>

        #make a new evaluator that goes along the if stmt and further
        new_f = new_body_evaluator(fnc.f, fnc.ast_root, fnc.symbolic_dict, fnc.pct, fnc.values_to_ret)
        eval_body(stmt.body, new_f)

       
        if new_f.values_to_ret:
            #append the values_to_ret, if there are some
            fnc.values_to_ret.append(new_f.values_to_ret)
            #flat the list
            fnc.values_to_ret = [item for sublist in fnc.values_to_ret for item in sublist]

        #ELSE Branch
        #negate the if stmt

        #TODOOOOOOO: this does not work, because the eval_expr_result is true and now false, somehow
        #fix: add a flag to the eval_expr function that negates the first statement ->
        # if flag is set, turn a > to a <= and so on
        eval_expr_result = eval_expr(stmt.test, fnc, True)

        print "Else condition: ", eval_expr_result


        #restore the pct
        fnc.pct = Solver()
        fnc.pct.assert_exprs(save_pct.assertions())

        #add the negation of the if stmt to the pct
        fnc.pct.add(eval_expr_result)

        print "Else pct", fnc.pct
        
        #<DEBUG>:
        if (fnc.pct.check() == sat):
            print "Model of the else clause: ", fnc.pct.model()
        #</DEBUG>

        #go on as if nothing happenend in the if block (hopefully, haha)
        eval_body(stmt.orelse, fnc)
        
        return
    
    #not sure if this works, have not tested it yet

    #TODO: there is a problem here!
    if type(stmt) == ast.Assign:
        assert (len(stmt.targets) == 1)  # Disallow a=b=c syntax
        lhs = stmt.targets[0]
        #print stmt.targets[0] #debug
        rhs = eval_expr(stmt.value, fnc, False)
        if type(lhs) == ast.Tuple:
            assert (type(rhs) == tuple)
            assert (len(rhs) == len(lhs.elts))
            for el_index in range(len(lhs.elts)):
                el = lhs.elts[el_index]
                assert (type(el) == ast.Name)
                fnc.symbolic_dict[el.id] = rhs[el_index]
            return
        if type(lhs) == ast.Name:
            fnc.symbolic_dict[lhs.id] = rhs
            return

    if type(stmt) == ast.Assert:
        # TODO: implement check whether the assertion holds.
        # However do not throw exception in case the assertion does not hold.
        # Instead return inputs that trigger the violation from SymbolicEngine.explore()

        #this should work, if the evaluation_to_pct is properly instantiated

        #save the current pct
        current_pct = Solver()
        current_pct.assert_exprs(fnc.pct.assertions())

        #evaluate this with eval_expr flag set to TRUE -> negate assertion
        # if its satisfiable, we have a model that violates the original assertion
        assertion_evaluation = eval_expr(stmt.test, fnc, True)
        print "Assertion evaluation: " , assertion_evaluation
        fnc.pct.add(assertion_evaluation)

        #check the new pct if the assertion does not hold
        if (fnc.pct.check() == sat):
            print ("We found a violating assertion")

            #TODO:
            #clean the model of all variables that are not inputs
            assertion_model = fnc.pct.model()

            assertion_dict = model_to_dictionary(assertion_model)

            assertion_dict = cleanup_dictionary_to_only_inputs(assertion_dict, fnc)

            fnc.assertion_violation_dict[stmt] = assertion_dict

            print "Assertion dict of violations so far:"
            print fnc.assertion_violation_dict

            #send the model to the parent if this is not the parent
            #assertion_violations_to_input needs to have the correct variables

        else:
            print "----------- True Assertion ---------------"

        #set the pct back to before the assertion, because the assertion should not influence our pct
        fnc.pct = Solver()
        fnc.pct.assert_exprs(current_pct.assertions())
        return
        
    raise Exception('Unhandled statement: ' + ast.dump(stmt))

#translates a string like     ((((x)+(y))==(0))and(((x)*(2))==(10)))or((a)or(not((b)==(False))))
#to   Or(And(x+y==0,x*2==10),Or(a,Not(b == False)))
#make sure, that variables like x are stored as Int('x')
#it might even not be a problem to store b also as an Int, because Bool is a subclass of Int
#attention to the only unary operation not!
#TODO: fill this in
def evaluation_to_pct (input_string, fnc):
    fnc.pct.add(True)
    # look at the brackets somehow
    return


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
        self.parents_of_all_children = True

        self.assertion_violation_dict = {}

        #make symbolic dictonary that has as key 'x' and as value '3' or '5/5 + y' (strings!)
        self.symbolic_dict = {}

        for i in range(0, len(f.args.args)):
            self.symbolic_dict[f.args.args[i].id] = f.args.args[i].id

        print "Symbolic dictionary:", 
        print self.symbolic_dict #debug
    
    #do not change
    def eval(self):
        run_body(self.f.body, self)
        
        assert (self.returned)
        return self.return_val

    def eval_symbolic(self):
        eval_body(self.f.body, self)
        
        assert (self.returned)
        return self.values_to_ret


####################
# Helper Functions #
####################

# f: function for which to generate inputs
# inputs: dictionary that maps argument names to values. e.g. {'x': 42 }
#do not change
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

#new
def new_body_evaluator(fnc, ast, symbolic_dict, pct, values_to_ret):
    new_input = generate_inputs(fnc, {})
    new_f = FunctionEvaluator(fnc, ast, new_input)
    new_f.symbolic_dict = symbolic_dict.copy()
    new_f.pct = Solver()
    new_f.pct.assert_exprs(pct.assertions())
    new_f.values_to_ret = values_to_ret [:]
    new_f.parents_of_all_children = False
    return new_f

#new
def cleanup_dictionary_to_only_inputs(in_dict, fnc):
    #print "Cleaning up", in_dict #debug
    input_keys = []
    for arg in fnc.f.args.args:
        assert (type(arg) == ast.Name)
        input_keys.append(arg.id)
    ret_dict = in_dict
    for k in ret_dict.keys():
        if k not in input_keys:
            del ret_dict[k]
    for elem in input_keys:
        if elem not in ret_dict:
            ret_dict[elem] = '0'
    return ret_dict

#do not change
def find_function(p, function_name):
    assert (type(p) == ast.Module)
    for x in p.body:
        if type(x) == ast.FunctionDef and x.name == function_name:
            return x
    raise LookupError('Function %s not found' % function_name)

#new, works
def model_to_dictionary(model):
    stmts = str(model).split(",")
    new_list = []
    for stmt in stmts:
        new_list.append("".join([char for char in stmt if (char not in [' ', '[', ']'])]))
    return {k:(Int(v)) for k,v in (x.split('=') for x in new_list) }


