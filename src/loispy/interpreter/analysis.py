from parsing import parse, AstNode
from symbol import Symbol, Sym
from symbol import _quote, _unquote, _quasiquote, _unquotesplicing, _let, _set,\
            _else, _lambdashorthand, _if, _begin, _vardef, _procdef, \
            _macrodef, _dict, _key
from environment import Environment, THE_GLOBAL_ENV
from procedure import Procedure
from codeobject import CodeObject
from builtin import builtin, builtinproc
from error import error, Error
from utils import to_string, isa
from re import findall


# ----------------------
# ANALYSIS AND EXECUTION
# ----------------------

# 'We split eval, which takes an expression and an environment, into two parts.
# The procedure analyze takes only the expression. It performs the syntactic
# analysis and returns a new procedure, the execution procedure, that
# encapsulates the work to be done in executing the analyzed expression.
# The execution procedure takes an environment as its argument and completes
# the evaluation. This saves work because analyze will be called only once on
# an expression, while the execution procedure may be called many times.'
# [ABELSON et al., 1996]


# save a reference to the python eval before we overwrite it.
python_eval = eval


def eval(_str, env=THE_GLOBAL_ENV):
    """
    Loispy eval (overwrites python eval)

    Parse a string, analyze all the expressions in the context of a given
    environment, and return the last resulting value

    @param str _str
    @param Environment env
    """
    return [analyze(e, toplevel=True).exec_(env) for e in parse(_str)][-1]


THE_GLOBAL_ENV.set("eval", builtinproc()(eval))


def analyze(astnode, toplevel=False):
    """
    Analyze an AstNode and return a CodeObject.

    'The result of calling analyze is the execution procedure
    to be applied to the environment [...] the procedures to which
    we dispatch perform only analysis, not full evaluation'
    [ABELSON et al., 1996]

    @param AstNode astnode
    @param bool toplevel

    @returns CodeObject
    """
    exp = astnode.exp
    # Atomic data types and symbols
    if self_eval(exp):
        return CodeObject(astnode, lambda env: exp)
    elif isa(exp, Symbol):
        return CodeObject(astnode, lambda env: env.find(exp)[exp])
    # Compound expressions
    elif isa(exp, list):
        if is_dict_literal(exp):
            return analyze_dict_literal(astnode)
        if is_if(exp):
            return analyze_if(astnode)
        elif is_begin(exp):
            return analyze_begin(astnode, toplevel)
        elif is_assignment(exp):
            return analyze_assignment(astnode)
        elif is_let(exp):
            return analyze_let(astnode)
        # elif is_lambda(exp):
        #     return analyze_lambda(astnode)
        elif is_lambda_shorthand(exp):
            return analyze_lambda_shorthand(astnode)
        elif is_vardef(exp):
            return analyze_vardef(astnode)
        elif is_procdef(exp):
            return analyze_procdef(astnode)
        elif is_macrodef(exp):
            return analyze_macrodef(astnode, toplevel)
        elif is_macro_application(exp):
            return analyze_macro_application(astnode)
        elif is_quoted(exp):
            return analyze_quotation(astnode)
        elif is_getter(exp):
            return analyze_getter(astnode)
        elif is_builtin_proc_application(exp):
            return analyze_builtin_proc_application(astnode)
        else:
            # If we haven't been able to determine an expression type so far,
            # we assume that it is a procedure call.
            return analyze_procedure_application(astnode)
    else:
        raise TypeError("Unknown expression type: %s, %s" %
                                                (str(type(exp)), exp))


# --------------------------
# EXPRESSION TYPE PREDICATES
# --------------------------


# Loispy uses data abstraction to 'decouple the general rules of operation
# from the details of how expressions are represented [...] this
# means that the syntax of the language being evaluated is determined solely
# by the procedures that classify and extract pieces of expressions'
# [ABELSON et al., 1996]
# 
# The following expression type predicates are used for classification.


def is_tagged(exp, tag):
    """
    Returns True if the first node of an <exp> is <tag>. Used in many other
    expression type predicates.

    @param str | Symbol tag
    @returns bool
    """
    if isa(exp, list) and isa(exp[0], AstNode):
        if isa(tag, Symbol):
            return exp[0].exp == tag
        else:
            return exp[0].exp is Sym(tag)

def self_eval(exp):
    return type(exp) in [int, bool, str, float, type(None)]

def is_begin(exp):
    return is_tagged(exp, _begin)

def is_if(exp):
    return is_tagged(exp, _if)

def is_let(exp):
    return is_tagged(exp, _let)

def is_vardef(exp):
    return is_tagged(exp, _vardef)

def is_procdef(exp):
    return is_tagged(exp, _procdef)

# def is_lambda(exp):
#     return is_tagged(exp, _lambda)

def is_lambda_shorthand(exp):
    return is_tagged(exp, _lambdashorthand)

def is_macrodef(exp):
    return is_tagged(exp, _macrodef)

def quoted(exp):
    return is_tagged(exp, _quote)

def unquoted(exp):
    return is_tagged(exp, _unquote)

def quasiquoted(exp):
    return is_tagged(exp, _quasiquote)

def unquoted_splicing(exp):
    return is_tagged(exp, _unquotesplicing)

def is_quoted(exp):
    return quoted(exp) or unquoted(exp) or quasiquoted(exp) \
           or unquoted_splicing(exp)

def is_macro_application(exp):
    return any([is_tagged(exp, macro) for macro in macro_table])

def is_builtin_proc_application(exp):
    return type(exp[0].exp) == Symbol and exp[0].exp in builtin

def is_getter(exp):
    return type(exp[0].exp) == Symbol and Sym(exp[0].exp)[0] == "."

def is_assignment(exp):
    return is_tagged(exp, _set)

def is_dict_literal(exp):
    return exp[0] is _dict


# --------------------
# TREATING EXPRESSIONS
# --------------------


def analyze_if(astnode):
    nodes = astnode.exp
    pred = analyze(nodes[1])
    then = analyze(nodes[2])
    if len(nodes) == 4:
        # there is an alternative expression to be evaluated
        alt = analyze(nodes[3]) 
    else:
        # If the tested predicate does not evaluate to #t, return #f
        alt = CodeObject(nodes[2], lambda env: False)
    return CodeObject(astnode, make_if(pred, then, alt))


def make_if(pred, then, alt):
    return lambda env: then.exec_(env) if pred.exec_(env) else alt.exec_(env)


def analyze_begin(astnode, toplevel):
    exps = [analyze(node, toplevel) for node in astnode.exp[1:]]
    def begin_(env):
        """
        Execute all the expressions in the begin block
        without returning a value
        """
        for e in exps:
            e.exec_(env)
        return None
    return CodeObject(astnode, begin_)


def analyze_let(astnode):
    exp = astnode.exp
    varexp = exp[1].exp
    if not len(varexp) or not all([len(node.exp) == 2 for node in varexp]):
        return error("Invalid vars for let: '%s'" % exp[1].tok)
    varnames = map(lambda node: node.exp[0].exp, varexp)
    analyzed = map(lambda node: analyze(node.exp[1]), varexp)
    exps = analyze_sequence(exp[2:])
    def _let(env):
        """
        Build a new env in which we define
        the evaluated vars, and evaluate the expressions
        in said env.
        """
        _vars = dict(zip(varnames,
                        map(lambda codeobj: codeobj.exec_(env), analyzed)))
        return exps(Environment(_vars, env))
    return CodeObject(astnode, _let)


def analyze_sequence(seq):
    exps = [analyze(e) for e in seq]
    last = exps.pop()
    def seq(env):
        """
        Evaluate all the expressions in a sequence, return the
        last resulting value
        """
        for e in exps:
            e.exec_(env)
        return last.exec_(env)
    return seq


def analyze_vardef(astnode):
    exp = astnode.exp
    var, val = exp[1].exp, analyze(exp[2])
    return CodeObject(astnode, lambda env: env.set(var, val.exec_(env)))


def analyze_procdef(astnode):
    exp = astnode.exp
    if not isa(exp[1].exp, list):
        procname, args, body = exp[1].exp, exp[2].get_exp(), exp[3:]
        proc = make_proc(args, body, procname)
        return CodeObject(astnode, lambda env: env.set(procname, proc(env)))
    else:
        procname, args, body = "", exp[1].get_exp(), exp[2:]
        return CodeObject(astnode, make_proc(args, body, procname))


# def analyze_lambda(astnode):
#     exp = astnode.exp
#     args, body = exp[1].get_exp(), exp[2:]
#     return CodeObject(astnode, make_proc(args, body))


def analyze_lambda_shorthand(astnode):
    args = findall("_\d{0,2}", to_string(astnode.exp[1].get_exp()))
    args = [Sym(a) for a in sorted(list(set(args)))]
    body = [astnode.exp[1]]
    return CodeObject(astnode, make_proc(args, body))


def make_proc(args, body, name=""):
    body = analyze_sequence(body)
    return lambda env: Procedure(env, args, body, name)


def analyze_procedure_application(astnode):
    exp = astnode.exp
    proc = analyze(exp[0])
    args = [analyze(node) for node in exp[1:]]
    def apply_proc(env):
        _args = [a.exec_(env) for a in args]
        _proc = proc.exec_(env)
        return _proc(*_args)
    return CodeObject(astnode, apply_proc)


def analyze_builtin_proc_application(astnode):
    """
    Used to bypass the environment lookup for builtin procedures
    """
    exp = astnode.exp
    proc = builtin[exp[0].exp]
    args = [analyze(node) for node in exp[1:]]
    return CodeObject(astnode, lambda env: proc(*[a.exec_(env) for a in args]))


def analyze_quotation(astnode):
    exp = astnode.exp
    text_of_quote = exp[1]
    if quoted(exp): # Just return the quoted value
        text_of_quote = text_of_quote.get_exp()
        return CodeObject(astnode, lambda env: text_of_quote)
    elif quasiquoted(exp):
        return CodeObject(astnode, expand_quasiquoted(text_of_quote.exp))
    else:
        raise SyntaxError("Invalid quotation")


def expand_quasiquoted(exp):
    # expansion has to happen at runtime (we need to access the actual
    # values being referenced), this is why expand_quasiquoted returns a
    # function.
    def expand(env):
        if not isa(exp, list):
            # Like quote, just return the quoted value.
            return exp
        elif unquoted(exp):
            return analyze(exp[1]).exec_(env)
        else:
            ret = []
            for node in exp:
                if unquoted_splicing(node.exp):
                    for item in expand_unquoted_splicing(node.exp, env):
                        ret.append(item)
                else:
                    ret.append(expand_quasiquoted(node.exp)(env))
            return ret
    return expand


def expand_unquoted_splicing(exp, env):
    res = analyze(exp[1]).exec_(env)
    if not hasattr(res, "__iter__"):
        raise Exception("Unquoted-splicing items must be iterable!")
    for item in res:
        yield item


def analyze_getter(astnode):
    exp = astnode.exp
    attr = exp[0].exp[1:]
    obj = analyze(exp[1])
    def _getattr(env):
        try:
            _obj = obj.exec_(env)
            _attr = getattr(_obj, attr)
        except AttributeError:
            return error("%s '%s' has no field '%s'" % (
                                type(_obj).__name__, _obj, attr))
        return _attr
    return CodeObject(astnode, _getattr)


def analyze_assignment(astnode):
    exp = astnode.exp
    if len(exp) != 3:
        return CodeObject(astnode,
                          lambda env: error("'set!' only takes two arguments"))
    else:
        var, val = exp[1].exp, analyze(exp[2])
        def set_(env):
            try:
                enclosing = env.find(var)
            except NameError as e:
                return Error(exc=e)
            enclosing.set(var, val.exec_(env))
        return CodeObject(astnode, set_)


def analyze_dict_literal(astnode):
    keys = [node.exp for node in astnode.exp[1]]
    values = [analyze(node) for node in astnode.exp[2]]
    def dict_(env):
        return dict(zip(keys, [val.exec_(env) for val in values]))
    return CodeObject(astnode, dict_)


# ------
# MACROS
# ------


macro_table = {}


class Macro(Procedure):
    def __str__(self):
        return "<Macro %s>" % self.name


def make_macro(macro_args, macro_body, macro_name):
    return Macro(THE_GLOBAL_ENV, macro_args, macro_body, macro_name)


def analyze_macrodef(astnode, toplevel):
    if not toplevel:
        raise SyntaxError("Macros can only be declared at top level")
    exp = astnode.exp
    macro_name = exp[1].exp
    macro_args = exp[2].get_exp()
    macro_body = analyze_sequence(exp[3:])
    macro = make_macro(macro_args, macro_body, macro_name)
    macro_table[macro_name] = macro
    return CodeObject(astnode, lambda env: env.set(macro_name, macro))


def macro_expand(macro, macro_args):
    return macro_table.get(macro)(*exp)


def analyze_macro_application(astnode):
    exp = astnode.exp
    macro, macro_args = exp[0].exp, astnode.get_exp()
    expanded = macro_expand(macro, macro_args)
    tostring = str(to_string(expanded))
    parsed = analyze(list(parse(tostring))[-1])
    return CodeObject(astnode, lambda env: parsed.exec_(env))
