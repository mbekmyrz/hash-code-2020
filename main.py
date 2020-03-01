def get_input(file):
    f = open(file, "r")
    lines = f.readlines()
    books_total = int(lines[0].split()[0])
    libraries_total = int(lines[0].split()[1])
    days_total = int(lines[0].split()[2])
    scores_books = list(map(int, lines[1].split()))

    inp_libraries = {}
    lib_id = 0
    for i in range(2, len(lines)):
        if i % 2 == 0:  # even lines contain library description
            lib = {}
            line = lines[i].split()
            if len(line) == 0:
                break
            lib["lib_id"] = lib_id
            lib["total_books"] = int(line[0])
            lib["signup_days"] = int(line[1])
            lib["per_day"] = int(line[2])
            lib["priority"] = 0.00
            lib["books"] = lines[i+1].split()
            lib["scanned_books"] = list()
            inp_libraries[str(lib_id)] = lib
            lib_id += 1
    f.close()
    return books_total, libraries_total, days_total, scores_books, inp_libraries


def write_output(file):
    f = open(file, "w+")
    scanned_libraries = len(library_order)
    f.write(str(scanned_libraries) + "\n")
    for lib in library_order:
        f.write(str(lib["lib_id"]) + " " + str(len(lib["scanned_books"])) + "\n")
        for x in lib["scanned_books"]:
            f.write(str(x + " "))
        f.write("\n")
    f.close()


def update_priorities(libs):
    for k in libs:
        if (remaining_days - libs[k]["signup_days"]) > 0:
            s = 0
            real_scan = (remaining_days - libs[k]["signup_days"]) * libs[k]["per_day"]
            for b in libs[k]["books"]:
                if b not in scanned_books:
                    s = s + books_scores[int(b)]
                    real_scan -= 1
                if real_scan == 0:
                    break
            libs[k]["priority"] = s / libs[k]["signup_days"]
        else:
            libs[k]["priority"] = 0


total_books, total_libraries, total_days, books_scores, libraries = get_input("e.txt")
library_order = []
scanned_books = set()
remaining_days = total_days

for i in range(total_libraries):
    libraries[str(i)]["books"].sort(key=lambda x: books_scores[int(x)], reverse=True)

while remaining_days > 0 and not len(libraries) == 0:
    update_priorities(libraries)
    max_index = max(libraries.keys(), key=lambda x: libraries[x]["priority"])
    remaining_days -= libraries[max_index]["signup_days"]
    n = remaining_days * libraries[max_index]["per_day"]
    index = 0
    while n > 0 and index < len(libraries[max_index]["books"]) and not len(libraries[max_index]["books"]) == 0:
        book = libraries[max_index]["books"][index]
        scanned_books.add(book)
        libraries[max_index]["scanned_books"].append(book)
        n -= 1
        index += 1
    if not len(libraries[max_index]["scanned_books"]) == 0:
        library_order.append(libraries[max_index].copy())
    print("Remained ", remaining_days, " days")
    libraries.pop(max_index)

write_output("e_out.txt")
