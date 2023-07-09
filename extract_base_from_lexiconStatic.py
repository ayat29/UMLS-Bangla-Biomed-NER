lexiconStatic = open("lexiconStatic2020", encoding = "utf-8", mode = "r")
lexiconStatic_base_extracted = open("lexiconStatic_base_extracted.txt", encoding = "utf-8", mode = "w")


for line in lexiconStatic.readlines():
    if line.startswith("{base"):
        lexiconStatic_base_extracted.write(line[line.find("=") + 1:])