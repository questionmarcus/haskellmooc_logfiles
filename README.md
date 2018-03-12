
# Anonymised logfiles from TryHaskell Servers

## Background

In 2016, the University of Glasgow ran a Haskell MOOC for the first
time. Check out
https://www.futurelearn.com/courses/functional-programming-haskell for
details.

We forked the tryhaskell REPL environment to allow our students to
experiment with interactive coding, for basic Haskell expressions and
program snippets. We captured the expressions submitted by the
students, to analyse them for pedagogical research.  Our tryhaskell
fork is at https://github.com/wimvanderbauwhede/haskelltutorials

## Functional Babytalk

Initial results are reported in our TFPIE 2017 paper, entitled
"Functional Babytalk" - see
https://www.cs.kent.ac.uk/people/staff/sjt/TFPIE2017/TFPIE_2017/Home.html
for details.

## Logfile Formatting

Here we publish the logfiles from the three AWS servers used for our
REPL. Each line is a single expression evaluation attempt, with the
format

T I > H

where T is a timestamp string, I is an integer representing a unique
IP address, and H is a Haskell expression. The let-bound variables are
automatically managed by our Javascript frontend, to enable name
bindings across multiple interactions.

## Reuse

Please feel free to use these log files for your own analysis
purposes. Please reference our TFPIE paper in any
publications/presentations you generate from your analysis.

Thanks,

Jeremy Singer
University of Glasgow
March 2018
http://www.dcs.gla.ac.uk/~jsinger

