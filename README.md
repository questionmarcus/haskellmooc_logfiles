
# Haskell MOOC log data and parsing scripts

## Requirements
1. An installation of Python >=3.4
2. The `regex` python library (not the standard `re` library)
3. A Haskell installation and the interactive Haskell compiler: `ghci`

All other Python libraries are included in the standard Python install, or with this repository.

## Getting started

1. Generate the tutorial help text map using `tutorial_scraper.py`
    * `./tutorial_scraper.py -i [<LIST OF .JS or .HTML FILES SEEN BY STUDENTS>] -o out_filename`
    * OR
    * `./tutorial_scraper.py --web -i [<LIST OF URLS WHERE .JS or .HTML FILES ARE STORED>] -o out_filename`
2. Generate JSON data from server logs using `jsonify.py`
    * `./jsonify.py --tut-data <FILEPATH TO OUTPUT FROM STEP 1> -i [<LIST OF SERVER LOG FILES>] -o <OUTPUT FILENAME PREFIX>`
    * Use the output file name prefix as the script generates two files:
        1. PREFIX-logdata.json with the parsed log data
        2. PREFIX-UserSessions.json with users session data (**EXPERIMENTAL FEATURE**)
    * **WARNING: THIS SCRIPT WILL TAKE A LONG TIME TO RUN DUE TO RUNNING OF ~335800 LINES OF HASKELL** (On a standard laptop this took ~6 hours for each year)
3. Use the JSON output for your own analysis or host the data in your own [api](https://github.com/questionmarcus/mooc-flask-api)

## Scripts included

|File Name|Description|
|--------|-----------|
|`anon.py`| Convert user IP addresses to integer IDs|
|`HaskellInterpreter.py`| Python class that acts as a façade to the GHCi and runs strings of Haskell data in the GHCi and returns the output|
|`jsonify.py`| Tool that takes server log files and combines them into JSON formatted data (run `./jsonify.py -h` for usage details|
|`log_to_tutorial_matcher.py`| Provides utility to match user input data to tutorial data based on information in help text |
|`RunTests.py`| Run the test suit, combining the tests in each of the `test_<script-name>/py`|
|`tutorial_scraper.py`| Utility that analyses javascript files used to create MOOC tutorial pages and finds all help text entered in `<code></code>` tags (run `tutorial_scraper.py -h` for usage details)|

## Background

In 2016, the University of Glasgow ran a Haskell MOOC for the first
time. Check out
[the course page on FutureLearn](https://www.futurelearn.com/courses/functional-programming-haskell) for
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

Marcus Lancaster &
Jeremy Singer
University of Glasgow
March 2018
http://www.dcs.gla.ac.uk/~jsinger

