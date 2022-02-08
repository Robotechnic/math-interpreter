from errorTypes import ErrorType

def displayError(error : str, error_type : ErrorType, at : int | range, message = "") -> None:
	"""
	Prints an error message to the console.
	
	Args:
		error (str): error message
		error_type (ErrorType): type of the error
		at (int | range): position of the error

		message (str): message to be displayed
		start (int): start of the error display
		end (int): end of the error display
	"""
	if type(error_type) != ErrorType:
		raise TypeError("error_type must be an ErrorType")
	
	print(f"{error_type.name} : {message}")


	print(error)
	if type(at) == int:
		print(" " * at + "^")
	elif type(at) == range:
		print(" " * at.start + "^" * (at.stop - at.start))

if __name__ == "__main__":
	displayError("5 / a - 7", ErrorType.SyntaxError, 4, message = "a is not defined")
	displayError("8 /* 5", ErrorType.ArithmeticExpressionError, range(2, 4))
	displayError("5 / 0", ErrorType.ZeroDivisionError, range(2, 5))