
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
    
def interpret(command: str):
    if command.startswith("select"):
        table = command.split("(")[1].split(",")[0].strip() 
        where = command.split(",")[1].strip("/n ")
        return f"q.select(obj_dict['{table}'], ','.join(obj_dict['{table}'].get_col_names()), '{where[:-1]}')"
    elif command.startswith("join"):
        tableA = command.split("(")[1].split(",")[0].strip()
        tableB = command.split("(")[1].split(",")[1].strip()
        where = command.split(",")[2].strip("/n")
        return f"q.join(obj_dict['{tableA}'], '{tableA}', obj_dict['{tableB}'], '{tableB}', '{where[:-1]}')"
    elif command.startswith("Hash"):
        table = command.split("(")[1].split(",")[0]
        ind = command.split(")")[0].split(",")[1]
        return (table, f"q.to_hash(obj_dict['{table}'], '{ind}')")
    elif command.startswith("Btree"):
        table = command.split("(")[1].split(",")[0]
        ind = command.split(")")[0].split(",")[1]
        return (table, f"q.to_btree(obj_dict['{table}'], '{ind}')")
    elif command.startswith("inputfrom"):
        file_path = command.split("(")[1].strip(")")        
        return f"Arrable().import_from_file(\'{file_path}\')"
    elif command.startswith("project"):
        table = command.split("(")[1].split(",")[0].strip()
        nargs = command.split(",")[1:]
        nargs[-1] = nargs[-1].strip(")")
        nargs = [f"'{arg.strip()}'" for arg in nargs]
        return "q.project(obj_dict['{}'], {})".format(table, *nargs)
    elif command.startswith('sum'):
        table = command.split("(")[1].split(",")[0].strip()
        param = command.split(",")[1].split(")")[0].strip()
        return f"q.sum(obj_dict['{table}'], '{param}')"
    elif command.startswith('avg'):
        table = command.split("(")[1].split(",")[0].strip()
        param = command.split(",")[1].split(")")[0].strip()
        return f"q.avg(obj_dict['{table}'], '{param}')"
    elif command.startswith('count'):
        table = command.split("(")[1].split(",")[0].strip()
        return f"q.count(obj_dict['{table}'])"
    elif command.startswith("sumgroup"):
        table = command.split("(")[1].split(",")[0].strip()
        param1 = command.split(',')[1]
        param2 = command.split(',')[2].split(")")[0]
        return f"q.sumgroup(obj_dict['{table}'], '{param1}', '{param2}')"
    elif command.startswith("avggroup"):
        table = command.split("(")[1].split(",")[0].strip()
        param1 = command.split(',')[1]
        param2 = command.split(',')[2].split(")")[0]
        return f"q.avggroup(obj_dict['{table}'], '{param1}', '{param2}')"
    elif command.startswith('countgroup'):
        table = command.split("(")[1].split(",")[0].strip()
        param = command.split(",")[1].split(")")[0].strip()
        return f"q.countgroup(obj_dict['{table}'], '{param}')"
    elif command.startswith("concat"):
        table1 = command.split("(")[1].split(",")[0].strip()
        table2 = command.split(",")[1].split(")")[0].strip()
        return f"q.concat(obj_dict['{table1}'], obj_dict['{table2}'])"
    elif command.startswith("outputtofile"):
        # outputtofile(T, T)
        table = command.split("(")[1].split(",")[0].strip()
        file_name = command.split(")")[0].split(",")[1].strip()
        return ('output_dummy', f"obj_dict['{table}'].output_to_file('{file_name}')")
    elif command.startswith("sort"):
        # sort(T1, S_C, col2, col3)
        table = command.split("(")[1].split(",")[0].strip()
        nargs = command.split(")")[0].split(",")[1:]
        nargs = [f"'{arg.strip()}'" for arg in nargs]
        return "q.sort(obj_dict['{table}'], {})".format(table=table, *nargs)
    elif command.startswith("movavg"):
        args = command.split("(")[1].split(")")[0]
        args = args.split(",")
        table = args[0].strip()
        col = args[1].strip()
        slider = args[2].strip()
        return f"q.movavg(obj_dict['{table}'], '{col}', {slider})"
    elif command.startswith("movsum"):
        args = command.split("(")[1].split(")")[0]
        args = args.split(",")
        table = args[0].strip()
        col = args[1].strip()
        slider = args[2].strip()
        return f"q.movsum(obj_dict['{table}'], '{col}', {slider})"
    # else:
    #     return "parse problem"