LOIS.PY
=======

This is my toy lisp learning project.

Name stands for *LO*ic's l*IS*p in *PY*thon.

The foundations of the code are heavily inspired by Abelsson, Sussman & Sussman's *Structure and Interpretation of Computer Programs* (SICP) & Peter Norvig's blogs, lis.py & lispy.py. I also sprinkled in some Clojure-like things, the implementation how-to of which intrigued me.

Mostly though, this will be a laboratory for me to conduct godawful experiments in lisp dialects interpretation.

PHILOSOPHY
----------

TBD


SYNTAX
------

### Procedures

    >> (=> my-proc (x) ())
    #n
    >> my-proc
    <Procedure my-proc>


Procedure call syntax is like any lisp:

    >> (my-proc 2)
    4


Procedures are first-class objects:

    >> (map my-proc `(1 2 3 4 5))
    (2 4 6 8 10)

Omitting the name in the procedure definition syntax returns an anonymous procedure ('lambda')

    >> (map (=> (x) (* x 2)) `(1 2 3 4 5))
    (2 4 6 8 10)


A clojure-like lambda shorthand syntax is provided:

    >> #(* _ _)
    <Procedure>
    >> (reduce #(+ _1 _2) (map #(* _ _) (range 100)))
    328350


### Variable definition and assignment

    >> ($ x 2)
    #n
    >> x
    2
    >> (set! x 4)
    #n
    >> x
    4


### Booleans & NoneType

    >> ($ t #t)
    #n
    >> (true? #t)
    #t
    >> (not #t)
    #f



### Lists

Loispy lists are Python lists.

    >> `(1 2 a "a" 3.0 #t)
    (1 2 a "a" 3.0 #t)

They can be declared using quotations, or the `list` built-in procedure.

    >> ($ my-list (list 1 2))
    #n
    >> my-list
    (1 2)
    >> (list? my-list)
    #t


### Dicts

Loispy dicts are python dicts.
Implementation is currently very rough, awful & buggy.

    >> {:hello "world" :this `is-cool :hi 5 :dat #t}
    {:hello "world" :this `is-cool :hi 5 :dat #t}


MACROS
------

Loispy provides scheme-like macros, defined using the `macro=>` keyword. Macros can only be defined at top-level, or within a `begin` block that is itself at top-level. macro-expand`-like procedure is yet to be implemented, but definitely will be (most of the stuff is there...)

Some of the loisp syntax (`cond`, `switch`, `let*`) is implemented using loisp macros. Here is, for instance, the macrodef for `let*`:

    (macro=> let* (vars body...)
      (=> expand (clauses body)
        (let ((first-clause (first clauses))
              (rest-clauses (all-but-first clauses)))
             (if (empty? rest-clauses)
                 `(let (,first-clause) ,@body)
                 `(let (,first-clause) ,(expand rest-clauses body)))))
      (expand vars body))



TESTING
-------

TBD

LICENSE
-------

TBD

