# Exercise 6

Since we have been discussing debugging, today we're going to analyze some code and see if we can figure out what's going wrong.

Here's our case study:

Alice is designing a prefix notation adding machine.

This machine uses parentheses and the plus sign to designate two arguments to add together.

Arguments must either be integers or another addition operation.

For example:

```lisp
(+ 1 1)          ; <1>
(+ 1 2)          ; <2>
(+ 2 (+ 3 3))    ; <3>
```

1. `<1>` this would yield `2`
2. `<2>` this would yield `3`
3. `<3>` this would yield `8`

You can find Alice's code in the class git repo `exercise_6` directory.

You'll also find it here for reference:

[parser.py](https://raw.githubusercontent.com/MattToegel/IS601/refs/heads/main/exercise_6/parser.py)

Run Alice's program and answer the following questions:

1. **In what function are you getting an error?**

   *There is an error in perfrom_operation(text) function. Inside that there is an issue with get_argument(text) function. The error returned is ValueError: invalid literal for int() with base 10: 'F'*

2. **What function called the function that's giving you an error?**

   *get_argument(text) function is called inside the function thats giving error*

3. **How many function calls in total were there before the error occurred?**

   *7 function calls happened before error*

4. **What is the type of error you're getting?**

   *The error received was ValueError : invalid literal for int() with base 10: 'F'*

5. **Is the error a problem with the parser or its input?**

   *The error is due to the input_text and parser as well because of letter 'F' which cannot be converted by int() in the input text and the parser could not parse ')'*

6. **If it's an input problem, how would you fix the input?**

   *The input problem can be fixed by removing 'F' from the input text.*

7. **If it's a parser problem, how would you fix the parser?**

   *I fixed the parser by making it handle cases where there is only one argument like (+3), The previous code assumed every operatin has two arguments.I modified the code to check after parsing the first argument if there is another argument to process or if it ')'. If it's a single argument, the parser should just return that value and move on. Additionally, I would ensure that the parser properly skips over the closing parenthesis after it finishes processing the arguments, whether it's one or two. This way the parser is corrected.*

8. **How could you make the parser raise a `ParserError` if this happens again in the future?**

   *I would add try / except block and raise ParserException in in the get_argument(text) function to raise ParserError in future*

9. **How many arguments does the addition operation in Alice's machine take?**

   *I would add try / except block and raise ParserException in in the get_argument(text) function to raise ParserError in functure*
