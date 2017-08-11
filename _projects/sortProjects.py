# this sorts projects first by last name, then by final or not, then by title

# files shortened as dictionaries with these keys:
#   filename
#   lastname
#   final
#   title
#   lines


import os, re


files = [ ]


# gather information on each file
for filename in os.listdir("."):
    if re.match(".*\.md", filename):
        with open(filename, "r") as f:
            lines = f.readlines()
            lastname = ""
            final = False
            title = ""
            # find lastname, final, and title properties of the file
            for line in lines:
                if re.match("lastName:.*", line):
                    lastname = line.replace("lastName:","").strip()
                if re.match("final:.*", line):
                    final = True
                if re.match("title:.*", line):
                    lastname = line.replace("title:","").strip()
            files.append({ "filename": filename, "lastname": lastname, "final": final, "title": title, "lines": lines });


# sort the list of files

def compare(file1, file2):
    if (file1["lastname"] < file2["lastname"]): return -1
    if (file1["lastname"] > file2["lastname"]): return 1
    # final is boolean, so checks are reversed (True < False)
    if (file1["final"] > file2["final"]): return -1
    if (file1["final"] < file2["final"]): return 1
    if (file1["title"] < file2["title"]): return -1
    if (file1["title"] > file2["title"]): return 1
    return 0

files.sort(compare)

# update file indices
for i, filehead in enumerate(files):
    # update index in header
    for j, line in enumerate(filehead["lines"]):
        if re.match("index:.*", line):
            filehead["lines"][j] = "index: " + str(i) + "\n"
            break
    # transfer update to the actual file
    with open(filehead["filename"], "w") as f:
        newcontent = "".join(filehead["lines"])
        f.write(newcontent)
