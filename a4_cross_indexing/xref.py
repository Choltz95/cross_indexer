from subprocess import call
from collections import defaultdict
import sys
import os
import errno
import re

log = "dwarf_log.txt"
statements = []
vars = defaultdict(list)
sub_programs = defaultdict(list)
symbol_table = {}
current_level = -1

name_stack = []
id_to_name = {}
all_vtypes = {}
vtypes = {}
enums = {}
all_vars = {}
all_local_vars = []
local_vars = []
anons = 0

 # Nasty, but appears to parse the lines we need
dwarf_header_regex = re.compile(r'<(?P<level>\d+)><(?P<statement_id>[0-9+]+)><(?P<type>\w+)>')
dwarf_key_val_regex = re.compile('\s*(?P<keyname>\w+)<(?P<val>[^>]*)>')

def create_directory(path):
    try:
        os.makedirs(path)
    except OSError, e:
        if e.errno != 17:
            print("file not created")

# feed line to input of the form <level><stmtid><type><key,val>
# ie <1><0x94><DW_TAG_variable> DW_AT_name<x> DW_AT_decl_file<0x00000001 /u/choltz2/school/csc_254/a4_cross_indexing/hello_world.c>
#    DW_AT_decl_line<0x00000005> DW_AT_type<<0x0000005b>> DW_AT_external<yes(1)> 
#    DW_AT_location<len 0x0009: 033810600000000000: DW_OP_addr 0x00601038>

def get_line(line):
    return 0

# process single dwarf statement
def parse_stmt(type, level, data, statement_id):
    new_level = int(level)
    if new_level > current_level:
        current_level = new_level
        name_stack.append([])
    elif new_level < current_level:
        name_stack = name_stack[:new_level+1]
        current_level = new_level

    name_stack[-1] = [type, statement_id]

    try:
        parent_kind, parent_name = name_stack[-2]
    except IndexError:
        parent_kind, parent_name = (None, None)

    if type == 'DW_TAG_variable' and level == '1':
        if 'DW_AT_location' in data:
            split = data['DW_AT_location'].split()
            if len(split) > 1:
                loc = int(split[1], 0)
                vars[data['DW_AT_name']] = [loc, data['DW_AT_type']]

def get_info(stmt):
    info_rgx = re.compile(r'<(-?[0-9]+)><(.*)><DW_TAG_(.*?)> .*DW_AT_name<(.*?)>')
    match = info_rgx.search(stmt)
    if match is not None:
        lvl = match.group(1)
        id = match.group(2)
        tag = match.group(3)
        name = match.group(4)
        # case subprogram
        if(tag == 'subprogram'):
            print 'matched subprogram'
        # case variable
        elif(tag == 'variable'):
            print 'matched variable'
        # unknown type
        else:
            #print 'unknown tag'
            return None
        return [lvl,id,tag,name]
    return None
'''
# case subprogram
    sub_program_rgx = re.compile(r'<(-?[0-9]+)><(.*)><DW_TAG_(subprogram)>')
    match = sub_program_rgx.search(stmt)
    if match is not None:
        print 'matched subprogram'
        print match.group(2)
        return 's'
# case variable
    sub_program_rgx = re.compile(r'<DW_TAG_variable>')
    if sub_program_rgx.search(stmt) is not None:
        print 'matched variable'
        return 'v'
'''
def parse_dd(statements):
    for stmt in statements:
        #print stmt
        info = get_info(stmt)
        if info is not None:
            if info[2] == "variable":
                vars[info[1]].append([info[0],info[2],info[3]])
            if info[2] == "subprogram":
                sub_programs[info[1]].append([info[0],info[2],info[3]])
    print vars
    print sub_programs

        #if get_info(stmt)[0] == "DW_TAG_subprogram":
            #print "yay"
            #sub_program_rgx = re.compile(r'<(level)><(type)>')
            #if sub_program_rgx.search(stmt) is not None:  

def generate_html(fname):
    r = open(fname, "r")
    w = open("HTML/"+fname[:-1]+"html", "w")
    w.write("<html><head></head><body><pre>")
    for line in r:
        w.write(line)
    w.write("</pre></body></html>")
    r.close()
    w.close()

def main():
    # save DD to log
    f = open(log, "w")
    call("~cs254/bin/dwarfdump -di " + str(sys.argv[1]), shell=True, stdout = f)
    f.close()
    # array of dd statements
    with open(log) as f:
        statements = f.readlines()
    parse_dd(statements)
    generate_html("hello_world.c")
    # create HTML directory
    create_directory("HTML")
main()