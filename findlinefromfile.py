class INFO():
    version = 0.2
    source = "https://stackoverflow.com/questions/4940032/how-to-search-for-a-string-in-text-files"
    author = "Accik"

def check(text, filename):
    n = 0
    with open(filename) as f:
        datafile = f.readlines()
    for line in datafile:
        n += 1
        if text in line:
            print("Line:", n)
            return True
    return False  # Because you finished the search without finding