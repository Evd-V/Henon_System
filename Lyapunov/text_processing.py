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

def write_data(fname, data, xsize=20, acc=3, delimiter='|', a=None, b=None, info=False, last=False):
    """ Function that writes data to a text file. The input parameter 'fname' denotes the 
        name of the text file. The data contains the data all in side a single list. 'xsize' 
        gives the number of data entries that will be printed in the x direction of the 
        table. 'acc' gives the number of decimal places that will be written in the file 
        for floats. 'delimiter' gives the separation between two different data entries; 
        this can only be one character. The input parameters 'a' and 'b' can be used to 
        write down extra information for each table. 'info' can be used to determine whether 
        or not some basic information at the top of the file should be printed. 'last' can 
        be used to denote that the last line of the file has been reached.
        
        Input:      fname     = name of the file that will be written (string);
                    data      = the input data that will be written to the file (list);
                    xsize     = the size of the written table in the x direction;
                    acc       = the accuracy of the printed floats (integer);
                    delimiter = separation between the data entries (string);
                    a         = provides extra information for the table (string);
                    b         = provides extra information for the table (string);
                    info      = determines if basic information should be printed (boolean);
                    last      = determines if the last line has been reached (boolean)
    """
    
    # Checking if 'acc' input parameter is valid
    if type(acc) != int:
        raise TypeError("'acc' input parameter must be an integer")
        
    # Checking if input parameter 'delimiter' is valid
    if len(delimiter) > 1:
        raise Exception("The 'delimiter' input can have a maximum length of 1")

    # Writing the data to the file
    with open(fname, "a") as f:
        
        # Checking if general information has to be provided
        if info:
            f.write("# This text file contains data in a two dimensional grid;\n")
            f.write(f"# Data written to file named {fname};\n")
            f.write(f"# The input size of the x columns is {xsize};\n")
            f.write("# The x dimension contains the 'b' values;\n")
            f.write("# The y dimension contains the 'a' values;\n")
        
        # Writing the header of each table
        if a.any() != None and b.any() != None:
            f.write(f"\n\nTABLE: {min(a)} < a < {max(a)} , {min(b)} < b < {max(b)} \n")
        else:
            f.write(f"\n\nTABLE\n")
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
            
        if last:
            f.write("EOF")
                                
# Escape sequence signs which can be ignored
# See for example: https://www.python-ds.com/python-3-escape-sequences
escape_seq = [" ", "\n", "\t", "\a", "\b", "\f", "\r", "\v", ","]

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
            if char == "a" or char == "b":
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
            
            # Checking if line is commented
            if comment in line:
                continue
            
            # Checking if we are dealing with a new table
            elif ("TABLE" in line) or ("EOF" in line):
                
                # Adding the header data to the 'headers' list
                if ind != len(lines):
                    evaluated_text = eval_text(line)
                    if len(evaluated_text) != 0:
                        headers.append(evaluated_text)
                
                # First checking if the 'current_data' list contains anything
                if len(current_data) == 0: continue
                
                # Adding the data of the previous table to 'all_data' and resetting the 'current_data' list
                all_data.append(current_data)
                current_data = []
                
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
                                
def rewrite_data(data, rewr_from, rewr_to):
    """ Function that rewrites two dimensional data by replacing 'rewr_from' values to 'rewr_to' 
        values.
        
        Input:      data      = the two dimensional data that will be rewritten (list);
                    rewr_from = the values that will be rewritten (float);
                    rewr_to   = the values that replace the rewr_from values (float);
                    
        Returns:    re_data   = the rewritten two dimensional data (list).
    """
    # Rewriting the data
    re_data = [[[rewr_to if k == rewr_from else k for k in j] for j in i] for i in data]
    
    return re_data
    
def comb_xdata(data):
    """ Function that combines data in the x direction. The input is a list containing for 
        example multiple tables which can have a different length. This function then adds 
        the first row of all tables in the first list; the second row in the second and so 
        on. The output is one list containing n separate lists, where n the length of the 
        largest table is.
        
        Input:      data     = the input data that will be combined in the x direction (list);
        
        Returns:    new_data = the combined data (list).
    """
    
    # Length of the first table, should be the same for all tables
    L = len(data[0])
    
    # Creating an empty list to put all the data in
    new_data = [[] for i in range(L)]
    
    # Looping over all tables
    for table in data:
        # Looping over all rows in each table
        for ind, row in enumerate(table):
            # Adding the row to the right list
            new_data[ind] += row
            
    return new_data
                                
def comb_data(data, xsize, ysize, rewr_from=9.9999, rewr_to=0.0000):
    """ Function that combines data such that it can be used for plotting. The input paramter 
        'data' gives the data that has to be combined. 'xsize' and 'ysize' determine how the 
        data should be combined in the x and y directions. 'rewr_from' and 'rewr_to' give the 
        user an option to rewrite certain data values (rewr_from) to other values (rewr_to).
        
        Input:      data      = the data that has to be combined (list);
                    xsize     = size of the combined data in the x direction (integer);
                    ysize     = size of the combined data in the y direction (integer);
                    rewr_from = values of the data that will be rewritten (float or None);
                    rewr_to   = values the above will be written to (float or None);
                    
        Returns:    full_data = the combined data (list).
    """
    
    # Rewrite the data to rewrite certain data entries
    rewr_data = rewrite_data(data, rewr_from, rewr_to)
    
    # List to put the combined data in
    full_data = []
    
    # The below results in 1 list containing all data points
    #for y in range(ysize):
    #    full_data += comb_ydata(comb_xdata(rewr_data[y*xsize:(y+1)*xsize]))
    
    # The below results in n lists containing n data points
    # Looping over the number of tables in the y direction
    for y in range(ysize):
        combined_xdata = comb_xdata(rewr_data[y*xsize:(y+1)*xsize])
        full_data += combined_xdata
        
    return full_data
                                
def analyse_headers(headers, keys):
    """ Function that analyses a list of headers to find the range of values. It 
        is assumed that the headers are dictionaries of which the keys are known. 
        The output is a list containing n lists, where n the length of 'keys' is, 
        and each list contains the range of values of that key.
        
        Input:      headers  = list containing the headers as a dictionary (list);
                    keys     = the keys of the header dictionaries (list or tuple);
                    
        Returns:    analysed = list containing the range of values in list form (list).
    """
    
    # Empty list to put the analysed headers in
    analysed = []
    
    # Looping over all keys
    for ind, key in enumerate(keys):
        # Finding the minimum and maximum of each header
        key_min = [min(header[ind][key]) for header in headers]
        key_max = [max(header[ind][key]) for header in headers]
        
        # List to put the unique values of the keys in
        leng = []
        
        # Looping over all values previously found
        for i in range(len(key_min)):
            # Checking if the entry already is present in the 'leng' list
            if key_min[i] not in leng:
                leng.append(key_min[i])
            elif key_max[i] not in leng:
                leng.append(key_max[i])
        
        # Adding the 'leng' list to the 'analysed' list
        analysed.append(leng)
            
    return analysed
