from subprocess import call
import sys
import os
import errno
import re

log = "dwarf_log.txt"
synbol_table = {}
current_level = -1
name_stack = []
id_to_name = {}
all_vtypes = {}
vtypes = {}
enums = {}
all_vars = {}
vars = {}
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
# ie
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


def parse_dd(log):
    f = open(log, "r")
    #for line in f:
        #print line,
    f.close()

def generate_html(fname):
    r = open(fname, "r")
    w = open("HTML/"+fname[:-1]+"html", "w")
    w.write("<html><head></head><body>")
    for line in r:
        w.write(line)
    w.write("</body></html>")
    r.close()
    w.close()

def main():
    print "hello world"
    # save DD to log
    f = open(log, "w")
    call("~cs254/bin/dwarfdump -i " + str(sys.argv[1]), shell=True, stdout = f)
    f.close()
    parse_dd(log)
    generate_html("hello_world.c")
    # create HTML directory
    create_directory("HTML")

main()
