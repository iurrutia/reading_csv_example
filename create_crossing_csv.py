import csv
from datetime import datetime
from operator import itemgetter





# path specifies the input csv
path = "Data.csv"

# path specifies the output csv
return_path = "report.csv"

# Initializes elements for tests
valid_Border = ['US-Canada Border','US-Mexico Border']




def process_csv(path):
    
    '''Reads the input csv file and populates the dictionary crossing_dict with keys and values.
    Keys are (border, measure) tuples.
    Values are (date, value) tuples.
    '''
    # process_csv reads each line of the input csv, and
    # for each line of the csv: 
    # - creates a crossing tuple key, then
    # - calls count_crossings to update crossing_dict
    
    # Initializes empty dictionary
    crossing_dict = {}

    with open(path, newline='') as file:
        reader = csv.reader(file)
        header = next (reader) # We denote the first line as the header of the csv file
        for i,row in enumerate(reader):
            row_information = process_row(i, row)
            
            if row_information is not None:
                # row_information has entries = (border, measure, date, value)
                
                # We store the Border, Measure, and Date temporarily as a 'crossing' tuple, 'current_crossing':
                current_crossing = (row_information[0], row_information[1], row_information[2])
                value = row_information[3]

                # We update crossing_dict
                count_crossing(current_crossing, value, crossing_dict)
            
    return crossing_dict
        
    
    
    
    
def process_row(i, row):
            
    # row = [string, string, string, Border, Date, Measure, Value, string]
    # For each row of the csv we read Border, Date and Measure

    # Read Border
    if row[3] in valid_Border:
        border = row[3]
    else:
        print("Row", i, "contains invalid Border value: ", row[3], "(Row ommited from totals.)")
        return None

    # Read Date
    try:
        date = datetime.strptime(row[4], '%m/%d/%Y %I:%M:%S %p')
    except ValueError:
        print("Row", i, "contains invalid Date value: ", row[4], "(Row ommited from totals.)")
        return None

    # Read Measure
    measure = row[5]

    # Read Value
    try:
        value = int(row[6])
    except ValueError:
        print("Row", i, "contains invalid format (not int): ", row[6], "(Row ommited from totals.)")
        return None

    return (border, measure, date, value)    
            

            
            
 

def count_crossing(key, value, crossing_dict):
    ''' Updates crossing_dict for each row of a csv.
    '''       
    # count_crossing updates crossing_dict values   
    crossing_dict[key] = crossing_dict.get(key,0) + value
        
        
        


def synth_crossings(crossing_dict):    
    ''' Creates a dictionary crossing_tally_dict with key/value pairs
     as follows: keys (Border, Measure) and values (Date, Value)
    '''
    # Initialize empty dictionary crossing_tally_dict:
    crossing_tally_dict = {}
    # Input dictionary d has key (Border, Date, Measure) and value (Value)
    for key in crossing_dict:
        # New key value is Border, Measure
        temp_key = (key[0],key[1])
        # We add tuples to the values of temp_key (Date, "Sum of crossings")
        if  temp_key in crossing_tally_dict:
            crossing_tally_dict[temp_key].append((key[2],crossing_dict[key]))
        else:
            crossing_tally_dict[temp_key] = [(key[2],crossing_dict[key])]
            
    return crossing_tally_dict



def add_running_avg(crossing_tally_dict):
    ''' Creates a sorted list (final_crossing_tally_list) of lists: 
    with items [Border, Date, Measure, Value, Average]  
    '''
    # Calculates the running average of crossings per border, measure pair
    # The input dictionary has keys (Border, Measure) and values (Date, Value)
    
    final_crossing_tally_list = []

    for key in crossing_tally_dict:
        crossing_tally_dict[key].sort()
        length = len(crossing_tally_dict[key])
        for i in range(length):
            if i == 0:
                temp_avg = 0
                temp_sum = 0
                # We add a list to final_crossing_tally_list in the format:
                # [Border, Date, Measure, Value, Average]
                final_crossing_tally_list.append([key[0], 
                                                  crossing_tally_dict[key][i][0],
                                                  key[1],
                                                  crossing_tally_dict[key][i][1],
                                                  temp_avg])
            else:
                temp_sum += crossing_tally_dict[key][i-1][1]
                temp_avg = round(temp_sum/(i))
                # We add a list to final_crossing_tally_list in the format:
                # [Border, Date, Measure, Value, Average]
                final_crossing_tally_list.append([key[0], 
                                                  crossing_tally_dict[key][i][0],
                                                  key[1],
                                                  crossing_tally_dict[key][i][1],
                                                  temp_avg
                                                 ])
    return final_crossing_tally_list


#######################################################################################


def main(path, return_path):
    # 1. Read in csv and count crossings per Border, Measure, Date
    crossing_dict = process_csv(path)

    # 2. Intermediate step to format the dictionary so it can be fed into step 3
    crossing_tally_dict = synth_crossings(crossing_dict)
    
    # 3. Calculate and add the running average:
    final_crossing_tally_list = add_running_avg(crossing_tally_dict)

    # 4. Sort to reorder the list to conform to the order specified by the problem outline:
    # Date (index 1), Value (index 3), Measure (index 2), and Border (index 0)
    final_crossing_tally_list.sort(key = itemgetter(1,3,2,0), reverse = True)    

    # 5. Write to new csv file
    with open(return_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(final_crossing_tally_list)
    file.close()
    
main(path, return_path)