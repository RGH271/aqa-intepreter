# Interpreter for AQA pseudocode

Dynamic interpreter for [AQA Pseudocode](https://filestore.aqa.org.uk/resources/computing/AQA-8525-NG-PC.PDF) for GCSE and A-Level.
This allows you to create a file in AQA pseudocode, that can be ran, to test to make sure it works without having to translate it into a runnable language such as python or c#.
It is hugely cobbled together so be prepared for bugs, especially as the program you're trying to run gets increasingly complex.

Ideally the files you put in should be *.aqac files, but it can be anything atm (i'll make it exclusive down the line).

## Usage

It is VERY unfinised, in the sense that it cant do much more than print statements, but if you wish to run it, then clone the repo, and then do:

```bash
cd aqa-interpreter
python3 main.py <your file>
```

inspired heavily by [slu4's video](https://www.youtube.com/watch?v=LgsW0eGk-6U)
