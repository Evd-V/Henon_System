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
