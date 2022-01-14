#!/bin/python3

# b2t.py -- BML to text (2021-12-30)
#           version 1 -- doesn't quite work, but almost...
#                        it'll have to do for now.
#
# This had got to be some of the ugliest code I've ever written.
# Well, I guess there is a first time for everything. Right?
# (LOL)


import sys
import re

spaces = "                                                            "
dashes = "------------------------------------------------------------"
dashesm = "————————————————————————————————————————————————————————————"
dashesn = "––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––"
macrons = "¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯"
upper8ths = "▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔"
hearts = "❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧❧"
doubledash = "════════════════════════════════════════════════════════════"
singledash = "────────────────────────────────────────────────────────────"
dashes = macrons
hearts = doubledash
mid = 44

def center(match_obj):
    if match_obj.group(1) is not None:
        text = match_obj.group(1)
        length = len(text)
        offset = int(mid-length/2)
        return spaces[:offset]+text+"\n"

def center_ff(match_obj):
    text = center(match_obj)
    return "\n\n" + text + "\f" + "\n"

def center_ff_frugal(match_obj):
    text = center(match_obj)
    return "\n" + text + "\f" + "\n"

def center_dashes(match_obj):
    if match_obj.group(1) is not None:
        text = match_obj.group(1)
        length = len(text)
        offset = int(mid-length/2)
        text1 = "\n"+spaces[:offset]+text+"\n"
        text2 = spaces[:offset]+dashes[:length]+"\n"+"\n\n"
        return text1+text2

def center_dashes_frugal(match_obj):
    if match_obj.group(1) is not None:
        text = match_obj.group(1)
        length = len(text)
        offset = int(mid-length/2)
        text1 = "\n"+spaces[:offset]+text+"\n"
        text2 = spaces[:offset]+dashes[:length]+"\n"
        return text1+text2

def center_hearts(match_obj):
    if match_obj.group(1) is not None:
        text = match_obj.group(1)
        length = len(text)
        offset = int(mid-length/2)
        text0 = "\n"+spaces[:offset]+hearts[:length]
        text1 = "\n"+spaces[:offset]+text+"\n"
        text2 = spaces[:offset]+hearts[:length]+"\n"+"\n"
        return text0+text1+text2

def center_hearts_frugal(match_obj):
    if match_obj.group(1) is not None:
        text = match_obj.group(1)
        length = len(text)
        offset = int(mid-length/2)
        text0 = "\n"+spaces[:offset]+hearts[:length]
        text1 = "\n"+spaces[:offset]+text+"\n"
        text2 = spaces[:offset]+hearts[:length]+"\n"
        return text0+text1+text2

PRE = 0
PARA = 1
VERSE = 2
render_mode = PARA

def format(line):
    global render_mode
    if line=="": return ""
    if "+" in line:   render_mode = PARA
    elif ">" in line: render_mode = VERSE
    elif "`" in line: render_mode = PRE
    elif "<" in line: render_mode = PARA
    elif line[0] == ")": render_mode = PARA
    if render_mode == PRE: 
        if line[0] == "`": return(line)
        elif line[0] == "/": return(line)
        else: return("`" + line)
    if render_mode == PARA: return(line)

    if line[0] == r"/": return(line)
    if line[0] == r"\\": return(line)
    if "#" in line: return(line)
    if line[0] == ">": return(line)
    if line[0] == ")": return(line)
    if line[0] == "}": return(line)
    orig_line = line

    line = re.sub(r"(\d) (\d)", r"\1@\2", line )

    line = re.sub(r"(\d )", r"\1     ", line)         # verse numbers
    line = re.sub(r"(\d\d )", r"\1", line)        # (unindented)
    line = re.sub(r"(\d[a-z] )", r"\1   ", line)
    line = re.sub(r"(\d\d[a-z] )", r"\1  ", line)
    line = re.sub(r"(\d\d\d )", r"\1", line)

    line = re.sub(r"(\d)@(\d)", r"\1 \2", line )

    if line == orig_line:
        line = "          " + orig_line

    return(line)

input_file = sys.argv[1]

with open(input_file) as f:
    buffer = f.read()

    line_list = buffer.split("\n")
    buffer = ""
    for line in line_list:
        buffer += format(line) + "\n"

# This is pretty cheesy. It sort of works. 
# If I had been more careful defining the markup language it would work better.
# Good enough for now?

# That said, this method is ridiculously fast, but horribly ugly. It's brand new 
# but already rotten. I don't want to change anything because, like I say,
# it sort of works.

    buffer = re.sub(r"\n\)", r"\n+]", buffer)               # ) -> +]
    buffer = re.sub(r"\n<", r"\n", buffer)                  # < -> nothing

    buffer = re.sub(r"\n}}(.+)\n", center_hearts_frugal, buffer)      # book title frugal
    buffer = re.sub(r"\n}(.+)\n", center_hearts, buffer)      # book title

    buffer = re.sub(r"###(.+)\n", center_hearts, buffer)           # headings
    buffer = re.sub(r"##(.+)\n", center, buffer)
    buffer = re.sub(r"#(.+)\n", center, buffer)

    buffer = re.sub(r"\\\\(.+)\n", center_ff_frugal, buffer)         # footers - form feed
    buffer = re.sub(r"\\(.+)\n", center_ff, buffer)         # footers - form feed
    buffer = re.sub(r"\\", r"\n\f", buffer)

    buffer = re.sub(r"\n//(.+)\n", center_dashes_frugal, buffer)    # frugal header
    buffer = re.sub(r"\n/(.+)\n", center_dashes, buffer)    # header

    buffer = re.sub(r"\n>(\d )", r"\n\1     ", buffer)          # numbered verses
    buffer = re.sub(r"\n>(\d\d )", r"\n\1     ", buffer)        # hmmm... same spacing as -^ ?
    buffer = re.sub(r"\n>(\d\d\d)", r"\n\1    ", buffer)

    buffer = re.sub(r"\n>>>(\d )", r"\n\1 " + spaces[:16], buffer)   # numbered verses
    buffer = re.sub(r"\n>>>(\d\d )", r"\n\1" + spaces[:16], buffer)
    buffer = re.sub(r"\n>>>(\d\d\d)", r"\n\1" + spaces[:16], buffer)

    buffer = re.sub(r"\n>\](\d\d\d)", r"\n\1.     ", buffer)
    buffer = re.sub(r"\n>\](\d\d)", r"\n\1.      ", buffer)      # (versified)
    buffer = re.sub(r"\n>\](\d)", r"\n\1.       ", buffer)       # chapter numbers

    buffer = re.sub(r"\n>>>>", r"\n" + spaces[:23], buffer) # other verses
    buffer = re.sub(r"\n>>>", r"\n" + spaces[:21], buffer)
    buffer = re.sub(r"\n>>", r"\n" + spaces[:12], buffer)
    buffer = re.sub(r"\n>", r"\n" + spaces[:10], buffer)

    buffer = re.sub(r"\n(\d )", r"\n\1   ", buffer)         # verse numbers
    buffer = re.sub(r"\n(\d\d )", r"\n\1  ", buffer)        # (unindented)
    buffer = re.sub(r"\n(\d[a-z] )", r"\n\1  ", buffer)
    buffer = re.sub(r"\n(\d\d[a-z] )", r"\n\1 ", buffer)
    buffer = re.sub(r"\n(\d\d\d )", r"\n\1 ", buffer)

    buffer = re.sub(r"\n\+(\d )", r"\n\1      ", buffer)    # verse numbers
    buffer = re.sub(r"\n\+(\d\d )", r"\n\1     ", buffer)   # (indented)
    buffer = re.sub(r"\n\+(\d[a-z] )", r"\n\1     ", buffer)
    buffer = re.sub(r"\n\+(\d\d[a-z] )", r"\n\1    ", buffer)
    buffer = re.sub(r"\n\+(\d\d\d )", r"\n\1    ", buffer)

    buffer = re.sub(r"\n\](\d\d\d) (\d) ", r"\n\1.\2 ", buffer)
    buffer = re.sub(r"\n\](\d\d) (\d) ", r"\n\1.\2 ", buffer)      # (unindented)
    buffer = re.sub(r"\n\](\d) (\d) ", r"\n\1.\2  ", buffer)       # chapter and verse numbers
    
    buffer = re.sub(r"\n\](\d\d\d) (\d\d) ", r"\n\1.\2", buffer)
    buffer = re.sub(r"\n\](\d\d) (\d\d) ", r"\n\1.\2", buffer)      # (unindented)
    buffer = re.sub(r"\n\](\d) (\d\d) ", r"\n\1.\2 ", buffer)       # chapter and verse numbers
    
    buffer = re.sub(r"\n\+\](\d\d\d) (\d) ", r"\n\1.\2   ", buffer)
    buffer = re.sub(r"\n\+\](\d\d) (\d) ", r"\n\1.\2    ", buffer) # (indented)
    buffer = re.sub(r"\n\+\](\d) (\d) ", r"\n\1.\2     ", buffer)  # chapter and verse numbers

    buffer = re.sub(r"\n\+\](\d\d\d) (\d\d) ", r"\n\1.\2  ", buffer)
    buffer = re.sub(r"\n\+\](\d\d) (\d\d) ", r"\n\1.\2   ", buffer) # (indented)
    buffer = re.sub(r"\n\+\](\d) (\d\d) ", r"\n\1.\2    ", buffer)  # chapter and verse numbers

    buffer = re.sub(r"\n\](\d\d\d) ", r"\n\1. ", buffer)
    buffer = re.sub(r"\n\](\d\d) ", r"\n\1.  ", buffer)      # (unindented)
    buffer = re.sub(r"\n\](\d) ", r"\n\1.   ", buffer)       # chapter numbers
    
    buffer = re.sub(r"\n\+\](\d\d\d) ", r"\n\1.    ", buffer)
    buffer = re.sub(r"\n\+\](\d\d) ", r"\n\1.     ", buffer) # (indented)
    buffer = re.sub(r"\n\+\](\d) ", r"\n\1.      ", buffer)  # chapter numbers

    buffer = re.sub(r"\+15b]2", "15b 2. ", buffer)          # special case Haggai

    buffer = re.sub(r"\n\+([a-zA-Z‘“(_—\[])", r"\n        \1", buffer)   # normal paragraph
    buffer = re.sub(r"\n([a-zA-Z‘“(_—\[])", r"\n     \1", buffer)        # normal text

    buffer = re.sub("\^", "", buffer)   # gobble the character formatting
    buffer = re.sub("_", "", buffer)
    buffer = re.sub("`", "", buffer)

# I don't believe we have to figure this out in the modern world.
# No form feed? Lines per page? Really?

    lines_per_page = 55
    line_list = buffer.split("\n")
    line_number = 0
    line_counter = 0
    line_max = len(line_list)
    while line_number < line_max:
        if line_list[line_number] != "\f":
            print(line_list[line_number])
            line_number += 1
            line_counter += 1
        else:
            line_number += 1
            while line_counter < lines_per_page:
                line_counter += 1
                print("")
            line_counter = 0
    
    #print(buffer, "", end="")

