## Exercise 6

1. There is an error in **perfrom_operation(text)** function. Inside that there is an issue with get_argument(text) function. The error returned is **ValueError: invalid literal for int() with base 10: 'F'**
2. **get_argument(text) function** is called inside the function thats giving error.
3. 7 function calls happened before error.
4. The error received was **ValueError** :  invalid literal for int() with base 10: 'F'
5. The error is due to the input_text and parser as well  because of letter 'F' which cannot be converted by int() in the input text and the parser could not parse ')' 
6. The input problem can be fixed by removing 'F' from the input text.
7. I fixed the parser by making it handle cases where there is only one argument like (+3), The previous code assumed every operatin has two arguments.I  modified the code to check after parsing the first argument if there is another argument to process or if it ')'. If it's a single argument, the parser should just return that value and move on. Additionally, I would ensure that the parser properly skips over the closing parenthesis after it finishes processing the arguments, whether it's one or two. This way the parser is corrected.
8. I would add try / except block and raise ParserException in in the get_argument(text) function to raise ParserError in functure.
9. The add operation takes two arguments and also nested single argument.
