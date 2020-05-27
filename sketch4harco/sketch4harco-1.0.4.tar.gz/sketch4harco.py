import nesterharco
man = []
other = []
try:
    #data = open('sketch.txt')
    with open('sketch.txt', 'r') as data:
        for each_line in data:
            try:
                (role, line_spoken) = each_line.split(':', 1)
                line_spoken = line_spoken.strip()
          
                if role == 'Man':
                    man.append(line_spoken)
                elif role == 'Other Man':
                    other.append(line_spoken)
            except ValueError:
                #print(each_line,  end =  '')
                pass

except IOError as err:
    print('The data file is missing:' + str(err))

try:
    with open("man_data.txt", "w") as man_file:
        nesterharco.print_lol(man, fn = man_file)

    with open("other_data.txt", 'w') as other_file:
        nesterharco.print_lol(other, fn = other_file)
    
except IOError as err:
    #print('File error.')
    print('File error: ' + str(err))


