
def save_labels(r, g, b, color_name):
    file_path = './label_info'
    f = open(file_path, 'a+')
    input_string = '%d %d %d %s\n' %(r, g, b, color_name)
    f.write(input_string)
    f.close()

def read_label():
    file_path = './label_info'
    f = open(file_path, 'r')
    X = []
    Y = []
    #Read file line by line
    line = f.readline()
    while line:
        r, g, b, color_name = line.split()
        r = int(r)
        g = int(g)
        b = int(b)
        X.append([r, g, b])
        Y.append(color_name)
        line = f.readline()
    f.close()

    return X, Y