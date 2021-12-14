# Lexer Project

Having a list of DFAs which defines the Lexem's tokens, we need to separate a given pattern into DFAs tokens.
If the pattern can be splitted into tokens, it means that the pattern is acceptable by DFAs.

# Input

Given an pattern and DFAs algorithm find the longest tokens accepted by DFAs and prints them.

# Output

<dfa_name> <accepted_symbols>

# Example

Given this pattern:

![pattern](https://user-images.githubusercontent.com/57661631/146004733-512dcec8-c95d-459f-b4ee-a7de9c974b31.png)

and 2 DFAs defined bellow:

![DFAs](https://user-images.githubusercontent.com/57661631/146004761-181869f4-3cc8-465b-b5fb-0c71dc76bd24.png)

Output file:


![lexems_out](https://user-images.githubusercontent.com/57661631/146004798-2db4c2e9-5520-4ed6-91a4-4b239dcb2b7f.png)
