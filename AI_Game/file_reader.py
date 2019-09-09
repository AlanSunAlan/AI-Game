
def readFile(file_path):
    result = []

    #Open file
    f = open(file_path, 'r')

    #Read file line by line
    line = f.readline()
    while line:
        value = int(line)
        result.append(value)
        line = f.readline()
    f.close()

    return result