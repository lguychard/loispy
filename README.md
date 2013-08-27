LOIS.PY
=======

This is my toy lisp project.

Name stands for LOic's lISp in PYthon.

The foundations of the code are heavily inspired by SICP & Peter Norvig's blogs, lis.py & lispy.py

Mostly though, this will be a laboratory for me to conduct godawful experiments in lisp dialects interpretation.




DATATYPES
=========

booleans & NoneType
-------------------

    

list
----

    >> `(1 2 a "a" 3.0 #t)
    (1 2 a "a" 3.0 #t)
    >> ($ my-list (list 1 2))
    #n
    >> my-list
    (1 2)
    >> (list? my-list)
    #t
    >> (map #(* _ 2) `(1 2 3 4 5))
    (2 4 6 8 10)

dict
----

    >> {:hello "world" :this `is-cool :hi 5 :dat #t}
    {:hello "world" :this `is-cool :hi 5 :dat #t}



