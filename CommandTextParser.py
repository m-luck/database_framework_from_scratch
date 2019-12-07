def remove_comments(line, sep):
    for s in sep:
        i = line.find(s)
        if i >= 0:
            line = line[:i]
    return line.strip()

def parse(input_path: str):
    with open(input_path) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    parsed = []
    for line in content:
        new_line = remove_comments(line, "//")
        if new_line != '':
            split_line = new_line.split(" := ", 1)
            parsed.append(split_line)
            
    return parsed
    
            
