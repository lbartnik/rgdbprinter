Pretty-printer for R in GDB
===========================

Compare output with the beautifier and without it.

### Call and closure

_With (re-formatted to fit inside a Markdown code block)_
```
#10 0x00007ffff787c9ac in Rf_applyClosure (
    call=g(c("a", "b"), 1, c(1.0, 2.0), True),
    op=<closure: a=, b=, c=, d=, { Sys.sleep(3.0) }>, 
    arglist=<promise: c("a", "b")>,
            <promise: 1>,
            <promise: c(1.0, 2.0)>,
            <promise: True>,
    rho=<environment>,
    suppliedvars=) at ../../../src/main/eval.c:1135
```

_Without (re-formatted to fit inside a Markdown code block)_
```
#10 0x00007ffff787c9ac in Rf_applyClosure (call=0x55555626bf18, 
                                           op=0x55555626b720,
                                           arglist=0x55555626c6d8,
                                           rho=0x55555626b818,
                                           suppliedvars=0x555555769b28)
    at ../../../src/main/eval.c:1135
```


### Bytecode and environment

_With_
```
#6  0x00007ffff788b67b in bcEval (body=<bytecode>,
                                  rho=<environment>,
                                  useCache=TRUE)
    at ../../../src/main/eval.c:5658
```

_Without_
```
#6  0x00007ffff788b67b in bcEval (body=0x55555626a110,
                                  rho=0x55555626c358,
                                  useCache=TRUE)
    at ../../../src/main/eval.c:5658
```


## Full backtrace


_With_
```
#0  0x00007ffff726ee83 in __select_nocancel () at ../sysdeps/unix/syscall-template.S:84
#1  0x00007ffff79be2ef in R_SelectEx (n=1, readfds=0x7ffff7dd5400 <readMask.11096>, writefds=0x0, exceptfds=0x0, timeout=0x7fffffffa170, intr=0x0)
    at ../../../src/unix/sys-std.c:154
#2  0x00007ffff79be652 in R_checkActivityEx (usec=3000000, ignore_stdin=1, intr=0x0) at ../../../src/unix/sys-std.c:331
#3  0x00007ffff79be6a1 in R_checkActivity (usec=3000000, ignore_stdin=1) at ../../../src/unix/sys-std.c:340
#4  0x00007ffff79c0766 in Rsleep (timeint=3) at ../../../src/unix/sys-std.c:1362
#5  0x00007ffff78e8c3e in do_syssleep (call=Sys.sleep(time), op=.Primitive(Sys.sleep), args=3.0, rho=<environment>) at ../../../src/main/platform.c:2997
#6  0x00007ffff788b67b in bcEval (body=<bytecode>, rho=<environment>, useCache=TRUE) at ../../../src/main/eval.c:5658
#7  0x00007ffff787b0d9 in Rf_eval (e=<bytecode>, rho=<environment>) at ../../../src/main/eval.c:616
#8  0x00007ffff787c9ac in Rf_applyClosure (call=Sys.sleep(3.0), op=<closure: time=, { <bytecode> }>, arglist=<promise: 3.0>, rho=<environment>, suppliedvars=)
    at ../../../src/main/eval.c:1135
#9  0x00007ffff787b8ac in Rf_eval (e=Sys.sleep(3.0), rho=<environment>) at ../../../src/main/eval.c:732
#10 0x00007ffff787c9ac in Rf_applyClosure (call=g(c("a", "b"), 1, c(1.0, 2.0), True), op=<closure: a=, b=, c=, d=, { Sys.sleep(3.0) }>, 
    arglist=<promise: c("a", "b")>, <promise: 1>, <promise: c(1.0, 2.0)>, <promise: True>, rho=<environment>, suppliedvars=) at ../../../src/main/eval.c:1135
#11 0x00007ffff787b8ac in Rf_eval (e=g(c("a", "b"), 1, c(1.0, 2.0), True), rho=<environment>) at ../../../src/main/eval.c:732
#12 0x00007ffff787c9ac in Rf_applyClosure (call=f(), op=<closure: a=, { g(c("a", "b"), 1, c(1.0, 2.0), True) }>, arglist=, rho=<environment>, suppliedvars=)
    at ../../../src/main/eval.c:1135
#13 0x00007ffff787b8ac in Rf_eval (e=f(), rho=<environment>) at ../../../src/main/eval.c:732
#14 0x00007ffff78be20e in Rf_ReplIteration (rho=<environment>, savestack=0, browselevel=0, state=0x7fffffffcbc0) at ../../../src/main/main.c:258
#15 0x00007ffff78be3d0 in R_ReplConsole (rho=<environment>, savestack=0, browselevel=0) at ../../../src/main/main.c:308
#16 0x00007ffff78bfe9f in run_Rmainloop () at ../../../src/main/main.c:1059
#17 0x00007ffff78bfeb5 in Rf_mainloop () at ../../../src/main/main.c:1066
#18 0x00005555555549c2 in main (ac=1, av=0x7fffffffdd08) at ../../../src/main/Rmain.c:29
#19 0x00007ffff71913f1 in __libc_start_main (main=0x555555554990 <main>, argc=1, argv=0x7fffffffdd08, init=<optimized out>, fini=<optimized out>, 
    rtld_fini=<optimized out>, stack_end=0x7fffffffdcf8) at ../csu/libc-start.c:291
#20 0x000055555555488a in _start ()
```


_Without_
```
#0  0x00007ffff726ee83 in __select_nocancel () at ../sysdeps/unix/syscall-template.S:84
#1  0x00007ffff79be2ef in R_SelectEx (n=1, readfds=0x7ffff7dd5400 <readMask.11096>, writefds=0x0, exceptfds=0x0, timeout=0x7fffffffa170, intr=0x0)
    at ../../../src/unix/sys-std.c:154
#2  0x00007ffff79be652 in R_checkActivityEx (usec=3000000, ignore_stdin=1, intr=0x0) at ../../../src/unix/sys-std.c:331
#3  0x00007ffff79be6a1 in R_checkActivity (usec=3000000, ignore_stdin=1) at ../../../src/unix/sys-std.c:340
#4  0x00007ffff79c0766 in Rsleep (timeint=3) at ../../../src/unix/sys-std.c:1362
#5  0x00007ffff78e8c3e in do_syssleep (call=0x55555626afd0, op=0x555555793978, args=0x55555626c320, rho=0x55555626c358) at ../../../src/main/platform.c:2997
#6  0x00007ffff788b67b in bcEval (body=0x55555626a110, rho=0x55555626c358, useCache=TRUE) at ../../../src/main/eval.c:5658
#7  0x00007ffff787b0d9 in Rf_eval (e=0x55555626a110, rho=0x55555626c358) at ../../../src/main/eval.c:616
#8  0x00007ffff787c9ac in Rf_applyClosure (call=0x55555626ab38, op=0x55555626a180, arglist=0x55555626c3c8, rho=0x55555626c470, suppliedvars=0x555555769b28)
    at ../../../src/main/eval.c:1135
#9  0x00007ffff787b8ac in Rf_eval (e=0x55555626ab38, rho=0x55555626c470) at ../../../src/main/eval.c:732
#10 0x00007ffff787c9ac in Rf_applyClosure (call=0x55555626bf18, op=0x55555626b720, arglist=0x55555626c6d8, rho=0x55555626b818, suppliedvars=0x555555769b28)
    at ../../../src/main/eval.c:1135
#11 0x00007ffff787b8ac in Rf_eval (e=0x55555626bf18, rho=0x55555626b818) at ../../../src/main/eval.c:732
#12 0x00007ffff787c9ac in Rf_applyClosure (call=0x55555626b968, op=0x55555626baf0, arglist=0x555555769b28, rho=0x5555557a1ff8, suppliedvars=0x555555769b28)
    at ../../../src/main/eval.c:1135
#13 0x00007ffff787b8ac in Rf_eval (e=0x55555626b968, rho=0x5555557a1ff8) at ../../../src/main/eval.c:732
#14 0x00007ffff78be20e in Rf_ReplIteration (rho=0x5555557a1ff8, savestack=0, browselevel=0, state=0x7fffffffcbc0) at ../../../src/main/main.c:258
#15 0x00007ffff78be3d0 in R_ReplConsole (rho=0x5555557a1ff8, savestack=0, browselevel=0) at ../../../src/main/main.c:308
#16 0x00007ffff78bfe9f in run_Rmainloop () at ../../../src/main/main.c:1059
#17 0x00007ffff78bfeb5 in Rf_mainloop () at ../../../src/main/main.c:1066
#18 0x00005555555549c2 in main (ac=1, av=0x7fffffffdd08) at ../../../src/main/Rmain.c:29
#19 0x00007ffff71913f1 in __libc_start_main (main=0x555555554990 <main>, argc=1, argv=0x7fffffffdd08, init=<optimized out>, fini=<optimized out>, 
    rtld_fini=<optimized out>, stack_end=0x7fffffffdcf8) at ../csu/libc-start.c:291
#20 0x000055555555488a in _start ()
```

