=== CSC 254 A3: Interpretation ===
Chester Holtz - 28264729 - choltz2@u.rochester.edu
Lee Murphy - 28250920 - lmurp14@u.rochester.edu

In this assignment we where required to implement an interpreter for programs written in an extended calculator language. A tokenizer, parser, and parse tree generator were provided. We implemented an ast generator, evaluator, repl, and simple variable matching.

== Files ==
README.txt - This file
interpreter.ml - parser logic to construct the syntax tree from tokens passed by the scanner and recover from any errors
grammar - file that details the extended calculator language - with ifs and whiles for our convenience.

== Description ==
This assignment tasked us with implementing a complete interpreter for an extended version of the calculator language in OCaml. The grammar is  included in the grammar file. We where provided with a parser generator and general driver by Professor Scott. Our specific task was to convert a parse tree into an explicit abstract syntax tree and then to evaluate the syntax tree.

A simple example program to read in a single literal and print would be
read a
write a
The parse tree for the above program looks as follows:
  PT_nt
   ("P",
    [PT_nt
      ("SL",
       [PT_nt ("S", [PT_term "read"; PT_id "a"]);
        PT_nt
         ("SL",
          [PT_nt
            ("S",
             [PT_term "write";
              PT_nt
               ("E",
                [PT_nt ("T", [PT_nt ("F", [PT_id "a"]); PT_nt ("FT", [])]);
                 PT_nt ("TT", [])])]);
           PT_nt ("SL", [])])]);
     PT_term "$$"])
and the associated syntax tree is computed as:
ast_sl = [AST_read "a"; AST_write (AST_id "a")]

for a more complex program to read in two numbers and compute their sum would be:
ast_sl =
	[AST_read "a"; AST_read "b";
		AST_assign ("sum", AST_binop ("+", AST_id "a", AST_id "b"));
		AST_write (AST_id "sum");
		AST_write (AST_binop ("/", AST_id "sum", AST_num "2"))]

What we want to do is generate the syntax tree associated with a parse tree and evaluate it - ie compute the correct output when
provided input for the above programs  

== Approach ==
For our approach we have a global memory environment which stores variables and assignments of "functions" and pass it through to each node of the ast.
We evaluate through each node, and if we encounter an error, we simply raise in ocaml and quit.

== Problems ==
Unfortunately, I had some problems reassigning variables in the memory. Instead, we just pass. I have a partial implementation which involves just appending, and parsing through the memory for the most recent assignments of variables. Since I was not able to complete this, although my while loop is syntactically and logically correct, it fails to iterate over a block when a program requires reassignment of a previously assigned variable.

== Instructions ==
from the command line, either run ocaml and #use "interpreter.ml";; 
or simply run ocaml with argument interpreter.ml (ocaml interpreter.ml)
make sure the ocaml path is established in your $PATH environment variable, or you have it aliased in your .bashrc/.cshrc.

== Example Output ==
A complex conditional program to compute if an input is 0 given as 
read a 
b := 3
mult := a * b
if (a + b) == b 
write 0 - 1
end 
if(a + b) != 0
write a + b"
end

If we run this program twice, providing arguments 4 and 0 respectively, we get output below:

- : unit = ()
val complex_cond_prog_parse_tree : parse_tree =
  PT_nt...
val complex_cond_prog_syntax_tree : ast_sl =
  [AST_read "a"; AST_assign ("b", AST_num "3");
   AST_assign ("mult", AST_binop ("*", AST_id "a", AST_id "b"));
   AST_if
    (("==", AST_binop ("+", AST_id "a", AST_id "b"), AST_id "b"),
     [AST_write (AST_binop ("-", AST_num "0", AST_num "1"))]);
   AST_if
    (("!=", AST_binop ("+", AST_id "a", AST_id "b"), AST_id "b"),
     [AST_write (AST_binop ("+", AST_id "a", AST_id "b"))]]);
7

- : unit = ()
-1
