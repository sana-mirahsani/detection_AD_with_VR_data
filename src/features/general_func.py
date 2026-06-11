import sys

def fail(msg: str, error:str ) -> None:
    """
    Function to match the error msg.
    Arg: 
        msg(str) : Message to print.
        error(str) : Type of Error.
    Return:
        None
    """
    match error:
        case "ValueError":
            raise ValueError(msg)
        case "Wrong type":
            raise TypeError(msg)
        case "Key not found":
            raise KeyError(msg)
        case "Index out of range":
            raise IndexError(msg)
        case "Something went wrong":
            raise RuntimeError(msg)
        case "File does not exist":
            raise FileNotFoundError(msg)
        case "Cannot divide by zero":
            raise ZeroDivisionError(msg)
        case "Feature not implemented":
            raise NotImplementedError(msg)
        case _:
            sys.exit("Unkown Error!!!")

def general_dict_check(input_dict: dict, input_dict_name: str, correct_keys: list):
    
    # check the general type
    if not isinstance(input_dict, dict):
        fail("Input is not a Dictionary!!!", "TypeError")
    
    # check the keys
    """missing = correct_keys - input_dict.keys()
    if missing:
        fail(f"Missing keys: {missing}", "ValueError")"""
    