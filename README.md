# Math-interpreter
A little math interpreter in python to graph functions and equations.

## How to use
This program is console only, you just need to start the main file and everithing will works. There is no need for external modules.

## Syntax
The syntax is similar to what you can write in a lot of others languages, there is math operators, functions and constants.
Allowed symbols are all lower case ascii letters, numbers and -/*<=>^()[;]

`a + b` will add a and b

`a - b` will substact b to a

`a * b` will multiply a peer b

`a / b` will divide a peer b

`a ^ b` will do a power b

`a == b` will return if a equal to b

`a <= b` will return if a is less than or equal to b

`a >= b` will return if a is greater than or equal to b

`a < b` will return if a is less than b

`a > b` will return if a is grater than b

`a <> b` will return if a is not equal to b

### function declaration
Syntax to create a new function is:
`name(arg[min;max][...],...) = expression`
Where:
- `name` is the name of the function
- `arg` is an argument name
- `[min;max]` is the allowed range of the argument, if you doesn't give any number, value will be infinite: `[1;]` mean "every number greater or equal than 1". You can also use open range to open range: `]1;]` mean every number greater than 1.
- `expression` is the function body

**Exemples**:

`f(x) = 2*x`

`f(x[0;]) = sqrt(2 * x) + 8`

`f(x[;1][1;]) = 1/x`

### Constants
|name|description|
|:--:|:---------:|
|pi|value of pi|
|e|value of exponential|
|tau|value of tau (around 2pi)|

### buildtin functions
There are are all basic math functions:
- sqrt
- sin
- cos
- tan
- acos
- asin
- atan
- atan2

And some spetial functions:

|name|description|
|:--:|:---------:|
|rad| convert degrees to radians|
|deg| convert radiand to degrees|
|abs| return absolute value of a number|
|plot| plot a function into borned graph|
|plot2d| plot a 2 paramaters function into a 2d graph|
|help| display function arguments and range |

### Exemples
![graph of tan(x^2+y^2) <= 5](https://github.com/Robotechnic/math-interpreter/raw/master/images/tan(x%5E2%2By%5E2)%3C%3D5.png)
![graph of sin(R)/R](https://github.com/Robotechnic/math-interpreter/raw/master/images/sin(R)%7CR.png)
