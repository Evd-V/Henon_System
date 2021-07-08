def conv_none_type(decimal, acc):
    """ Function that creates a number containing only one number between 0 and 9 (both 
        included). The input parameter 'decimal' denotes which number this will be. The 
        input paramter 'acc' determines the number of times the 'decimal' number is 
        copied. For example, if we have 'decimal = 9' and 'acc = 3' the output will be: 
        9.99. This can be useful to change 'None' type values into integers.
        
        Input:      decimal = the decimal which will be printed (integer);
                    acc     = the number of decimal places (integer);
                    
        Returns:    value   = the newly created number (float).
    """
    
    # Checking if the input parameter 'decimal' is an integer
    if type(decimal) != int:
        raise TypeError("The input paramter 'decimal' must be an integer")
    
    # Checking if the input parameter 'acc' is an integer
    if type(acc) != int:
        raise TypeError("The input paramter 'acc' must be an integer")
    
    # Checking if the input parameter decimal is a valid integer
    if 0 > decimal or decimal > 9:
        raise TypeError("The input parameter 'decimal' must be an integer in the range from 0 to 9")
    
    # Creating the new value
    value = decimal
    
    # Adding the number of decimal places
    for i in range(acc):
        value += decimal * 10**(-(i+1))
    
    return value

def write_data(fname, data, xsize=20, acc=3, delimiter='|', a=None, b=None, info=True):
    """ Function that writes data to a text file. The input parameter 'fname' denotes the 
        name of the text file. The data contains the data all in side a single list. 'xsize' 
        gives the number of data entries that will be printed in the x direction of the 
        table. 'acc' gives the number of decimal places that will be written in the file 
        for floats. 'delimiter' gives the separation between two different data entries; 
        this can only be one character. The input parameters 'a' and 'b' can be used to 
        write down extra information for each table. 'info' can be used to determine whether 
        or not some basic information at the top of the file should be printed.
        
        Input:      fname     = name of the file that will be written (string);
                    data      = the input data that will be written to the file (list);
                    xsize     = the size of the written table in the x direction;
                    acc       = the accuracy of the printed floats (integer);
                    delimiter = separation between the data entries (string);
                    a         = provides extra information for the table (string);
                    b         = provides extra information for the table (string);
                    info      = determines if basic information should be printed (boolean);
    """
    
    # Checking if 'acc' input parameter is valid
    if type(acc) != int:
        raise TypeError("'acc' input parameter must be an integer")
        
    # Checking if input parameter 'delimiter' is valid
    if len(delimiter) > 1:
        raise Exception("The 'delimiter' input can have a maximum length of 1")

    # Writing the data to the file
    with open(fname, "w+") as f:
        
        # Checking for already provided data
        lines = f.readlines()
        
        # Number of tables
        no_tables = 0
        
        # Finding the number of tables (still does not work)
        for line in lines:
            if "TABLE" in line:
                no_tables += 1
        
        # Checking if general information has to be provided
        if info:
            f.write("This text file contains data in a two dimensional grid;\n")
            f.write(f"Data written to file named {fname};\n")
            f.write(f"The input size of the x columns is {xsize};\n")
            f.write(f"This file contains {no_tables} tables;\n")
            f.write(80*"-")
            f.write("\n\n")
        
        # Writing the header of each table
        if a != None and b != None:
            f.write(f"TABLE #{no_tables + 1}, {a[0]} < a < {a[1]}, {b[0]} < b < {b[1]} \n")
        else:
            f.write(f"TABLE #{no_tables + 1}\n")
        f.write("\n")
        
        # Writing the data
        for i in range(0, len(data), xsize):
            for j in data[i:i+xsize]:
                if j == None:
                    conv_none = conv_none_type(9, acc)
                    f.write(f" {conv_none} {delimiter}")
                    continue
                elif j < 0:
                    f.write(f"{j:.{acc}f} {delimiter}")
                else:
                    f.write(f" {j:.{acc}f} {delimiter}")
            f.write("\n")
                                
# Escape sequence signs which can be ignored
# See for example: https://www.python-ds.com/python-3-escape-sequences
escape_seq = [" ", "\n", "\t", "\a", "\b", "\f", "\r", "\v"]

# List of mathematical characters which can often be ignored
math_char = ["<", ">", "-", "+", "/", "*", "^", "**", "=", "<=", ">="]

def eval_text(string):
    """ Function that evaluates a string expression. This function is especially useful 
        to find the headers of files creating using the 'write_data' function defined 
        above. The output is a list with dictionaries.
        
        Input:      string = string that will be analysed (string);
        
        Returns:    dicts  = list containing the data in dictionaries (list).
    """
    
    # Splitting by spaces
    red_string = string.split(" ")
    
    # List to put data in
    vals = []
    misc = []
    
    # Looping over all splitted strings
    for char in red_string:
        # Checking if word or character can be ignored
        if char == "TABLE:" or char in (math_char or escape_seq): continue
        
        # All other cases
        else:
            if char == 'a' or char == 'b':
                misc.append(char)
            else:
                try:
                    vals.append(eval(char))
                except:
                    continue
                
    # List to put dictionaries in   
    dicts = []
    
    # Creating the dictionaries
    for ind, c in enumerate(misc):
        try:
            dicts.append({c: [vals[2*ind], vals[2*ind+1]]})
        except:
            raise Exception("Invalid header input")
        
    return dicts

def read_data(fname, comment="#", delimiter="|"):
    """ Function that reads data from a given file. This function works best combined 
        with the files that are written using the 'write_data' function defined above. 
        The input parameter 'comment' gives the character which determines the 
        commented lines that can be ignored. The 'delimiter' paramter gives the character 
        which separates two different values in a table.
        
        Input:      fname     = name of the file that will be read (string);
                    comment   = character that gives which lines are commented (string);
                    delimiter = character that gives how two values are separated (string);
                    
        Returns:    all_data  = the data that is obtained after reading the table (list).       
    """
    
    # Reading the file
    with open(fname, "r") as f:
        
        # Reading the lines
        lines = f.readlines()
        
        # Lists to put the data in
        current_data = []
        all_data = []
        
        # List to put the headers in
        headers = []
        
        # Looping over all lines
        for ind, line in enumerate(lines):
            
            # Checking if we are dealing with a new table
            if ("TABLE" in line) or (ind == len(lines)-1):
                
                # Adding the header data to the 'headers' list
                if ind != len(lines)-1:
                    headers.append(eval_text(line))
                
                # First checking if the 'current_data' list contains anything
                if len(current_data) == 0: continue
                
                # Adding the data of the previous table to 'all_data' and resetting the 'current_data' list
                all_data.append(current_data)
                current_data = []
                
            # Checking if line is commented
            elif comment in line:
                continue
                
            else:
                # Splitting the lines according to the delimiter
                data = line.split(delimiter)
                
                # List to put the data of each line in
                red_data = []
                
                # Looping over the characters in the line
                for i in data:
                    if i in escape_seq: continue
                    else:
                        try:
                            red_data.append(eval(i))
                        except:
                            red_data.append(conv_none_type(9, 4))
                            
                # Checking if there is any data that has to be added
                if len(red_data) != 0:
                    current_data.append(red_data)
                
        return all_data, headers
