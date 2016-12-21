"""
Pretty-prints arguments to R functions by traversing heap and
following R internal structures.
Tested with GDB 7.11.90
"""

import gdb

# ----------------------------------------------------------------------

_have_gdb_printing = True
try:
    import gdb.printing
except ImportError:
    _have_gdb_printing = False

try:
    from gdb.types import get_basic_type
except ImportError:
    # from libstdcxx printers
    def get_basic_type(type):
        # If it points to a reference, get the reference.
        if type.code == gdb.TYPE_CODE_REF:
            type = type.target()
        # Get the unqualified type, stripped of typedefs.
        type = type.unqualified().strip_typedefs()
        return type


# ----------------------------------------------------------------------

class SEXPPrinter(object):
    "Print a SEXP object"

    def __init__(self):
        self.name = 'SEXP'
        self.enabled = True
    
    def __call__(self, value):
        basic_type = get_basic_type(value.type)
        if basic_type and 'SEXP' in str(basic_type):
            return SEXP(value)
        return None


# ----------------------------------------------------------------------

class Types:
    "Shortcuts to handy C types"

    void_ptr_t    = gdb.lookup_type('void').pointer()
    char_ptr_t    = gdb.lookup_type('char').pointer()
    int_ptr_t     = gdb.lookup_type('int').pointer()
    double_ptr_t  = gdb.lookup_type('double').pointer()
    sexp_ptr_t    = gdb.lookup_type('SEXP').pointer()


# ----------------------------------------------------------------------

class R:

    def type(n):
        "Types as defined in Rinternals.h"
        return {
            0:  "NILSXP",     # nil = NULL
            1:  "SYMSXP",     # symbols
            2:  "LISTSXP",    # lists of dotted pairs
            3:  "CLOSXP",     # closures
            4:  "ENVSXP",     # environments
            5:  "PROMSXP",    # promises: [un]evaluated closure arguments
            6:  "LANGSXP",    # language constructs (special lists)
            7:  "SPECIALSXP", # special forms
            8:  "BUILTINSXP", # builtin non-special forms
            9:  "CHARSXP",    # "scalar" string type (internal only)
            10: "LGLSXP",     # logical vectors
            13: "INTSXP",     # integer vectors
            14: "REALSXP",    # real variables
            15: "CPLXSXP",    # complex variables
            16: "STRSXP",     # string vectors
            17: "DOTSXP",     # dot-dot-dot object
            18: "ANYSXP",     # make "any" args work
            19: "VECSXP",     # generic vectors
            20: "EXPRSXP",    # expressions vectors
            21: "BCODESXP",   # byte code
            22: "EXTPTRSXP",  # external pointer
            23: "WEAKREFSXP", # weak reference
            24: "RAWSXP",     # raw bytes
            25: "S4SXP",      # S4 non-vector

            30: "NEWSXP",     # fresh node creaed in new page
            31: "FREESXP",    # node released by GC

            99: "FUNSXP",     # Closure or Builtin
        }.get(int(n), 'unknown')

    def NilValue():
        gdb.lookup_global_symbol("R_NilValue").value()

    def UnboundValue():
        gdb.lookup_global_symbol("R_UnboundValue").value()

    def car(val):
        return val['u']['listsxp']['carval']

    def cdr(val):
        return val['u']['listsxp']['cdrval']
    
    def tag(val):
        return val['u']['listsxp']['tagval']

    def printname(val):
        return val['u']['symsxp']['pname']

    def prim_name(val):
        # R_FunTab[(x)->u.primsxp.offset].name
        fun_tab = gdb.lookup_global_symbol("R_FunTab").value()
        offset  = int(val['u']['primsxp']['offset'])
        return ".Primitive(%s)" % (fun_tab[offset]['name'].string())

    def prcode(val):
        return val['u']['promsxp']['expr']

    def formals(val):
        return val['u']['closxp']['formals']

    def body(val):
        return val['u']['closxp']['body']

    def dataptr(val):
        adr = val['u'].address.cast(Types.int_ptr_t) + 2
        return adr.cast(Types.void_ptr_t)

    def char_value(val):
        return str(R.dataptr(val).cast(Types.char_ptr_t).string())

    def length(val):
        adr = val['u'].address.cast(Types.int_ptr_t)
        return int(adr.dereference())

    def logical_elt(val, i):
        adr = R.dataptr(val).cast(Types.int_ptr_t) + i
        return bool(adr.dereference())

    def integer_elt(val, i):
        adr = R.dataptr(val).cast(Types.int_ptr_t) + i
        return int(adr.dereference())
    
    def real_elt(val, i):
        adr = R.dataptr(val).cast(Types.double_ptr_t) + i
        return float(adr.dereference())
    
    def string_elt(val, i):
        adr = R.dataptr(val).cast(Types.sexp_ptr_t) + i
        return R.char_value(adr.dereference())


# ----------------------------------------------------------------------

class SEXP:
    "Wrapper for a SEXP object"
    
    def __init__(self, val):
        self.val  = val
        self.type = R.type(int(val['sxpinfo']['type']))
    
    def __str__(self):
        return self.to_string()

    def to_string(self):
        if self.val == R.NilValue():
            return "(Nil)"
        if self.val == R.UnboundValue():
            return "(Unbound)"
        
        method = {
            "NILSXP":     lambda: "",          # 0
            "SYMSXP":     self.sym_sxp,        # 1
            "LISTSXP":    self.list_sxp,       # 2
            "CLOSXP":     self.clo_sxp,        # 3
            "ENVSXP":     self.env_sxp,        # 4
            "PROMSXP":    self.prom_sxp,       # 5
            "LANGSXP":    self.lang_sxp,       # 6
            "BUILTINSXP": self.builtin_sxp,    # 8
            "CHARSXP":    self.char_sxp,       # 9
            "LGLSXP":     self.lgl_sxp,        # 10
            "INTSXP":     self.int_sxp,        # 13
            "REALSXP":    self.real_sxp,       # 14
            "STRSXP":     self.str_sxp,        # 16
            "BCODESXP":   lambda: "<bytecode>" # 21
        }.get(self.type, self.unsupported)
        return method()
    
    def unsupported(self):
        return "unsupported type " + str(self.type)

    def vector(self, type_method):
        "Generic vector support"
        values = [type_method(self.val, i) for i in range(R.length(self.val))]
        if len(values) == 0:
            return "c()"
        if len(values) == 1:
            return str(values[0])
        return '[' + ', '.join([str(v) for v in values]) + ']'

    # --- SYMSXP -------------------------------------------------------
    def sym_sxp(self):
        "Print symbol, type 1"
        return SEXP(R.printname(self.val)).to_string()

    # --- LISTSXP ------------------------------------------------------
    def list_sxp(self):
        "Print list object, type 2"
        car = SEXP(R.car(self.val))
        carstr = car.to_string()

        tag = SEXP(R.tag(self.val))
        if tag.type != 'NILSXP':
            carstr = '%s=%s' % (tag.to_string(), carstr)

        cdr = SEXP(R.cdr(self.val))
        if cdr.type == "NILSXP":
            return carstr
        return '%s, %s' % (carstr, cdr.to_string())

    # --- LISTSXP ------------------------------------------------------
    def clo_sxp(self):
        "Print closure, type 3"
        body = SEXP(R.body(self.val))
        formals = SEXP(R.formals(self.val))
        return '<closure: %s, { %s }>' % (formals.to_string(), body.to_string())

    # --- LISTSXP ------------------------------------------------------
    def env_sxp(self):
        "Print environment, type 4"
        return "<environment>"

    # --- PROMSXP ------------------------------------------------------
    def prom_sxp(self):
        "Print promise, type 5"
        return "<promise: %s>" % R.prcode(self.val)

    # --- LANGSXP ------------------------------------------------------
    def lang_sxp(self):
        "Print language object, type 6"
        car = SEXP(R.car(self.val))
        cdr = SEXP(R.cdr(self.val))
        return "%s(%s)" % (car.to_string(), cdr.to_string())

    # --- CHARSXP ------------------------------------------------------
    def builtin_sxp(self):
        "Print built-in valu, type 8"
        return R.prim_name(self.val)

    # --- CHARSXP ------------------------------------------------------
    def char_sxp(self):
        "Print char value, type 9"
        return R.char_value(self.val)

    # --- LGLSXP -------------------------------------------------------
    def lgl_sxp(self):
        "Print logical vector, type 10"
        return self.vector(R.logical_elt)

    # --- INTSXP -------------------------------------------------------
    def int_sxp(self):
        "Print integer vector, type 13"
        return self.vector(R.integer_elt)

    # --- REALSXP ------------------------------------------------------
    def real_sxp(self):
        "Print double vector, type 14"
        return self.vector(R.real_elt)

    # --- STRSXP ------------------------------------------------------
    def str_sxp(self):
        "Print string vector, type 16"
        return self.vector(lambda v,i: '"%s"' % R.string_elt(v,i))


# ----------------------------------------------------------------------

def register_sexp_printer(obj):
    "Register printer generator with objfile obj."

    global printer_gen

    if _have_gdb_printing:
        gdb.printing.register_pretty_printer(obj, SEXPPrinter(), replace=True)
    else:
        if obj is None:
            obj = gdb
        obj.pretty_printers.append(printer_gen)

register_sexp_printer(gdb.current_objfile())
