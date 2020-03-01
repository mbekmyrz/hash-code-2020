import statistics


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
    total_scanned_libraries = len(library_order)
    f.write(str(total_scanned_libraries) + "\n")
    for lib in library_order:
        f.write(str(lib["lib_id"]) + " " + str(len(lib["scanned_books"])) + "\n")
        for x in lib["scanned_books"]:
            f.write(str(x + " "))
        f.write("\n")
    f.close()


def update_priorities(rem_days, libs, sc_books):
    scores = list()
    for k in libs:
        if (rem_days - libs[k]["signup_days"]) > 0:
            s = 0
            real_scan = (rem_days - libs[k]["signup_days"]) * libs[k]["per_day"]
            for b in libs[k]["books"]:
                if b not in sc_books:
                    s = s + books_scores[int(b)]
                    real_scan -= 1
                if real_scan == 0:
                    break
            libs[k]["priority"] = s
            scores.append(s)
        else:
            libs[k]["priority"] = 0
            scores.append(0)

    stdev = statistics.variance(scores)
    for k in libs:
        if (rem_days - libs[k]["signup_days"]) > 0:
            libs[k]["priority"] = libs[k]["priority"] ** 2 / (stdev * libs[k]["signup_days"])
        else:
            libs[k]["priority"] = 0

    return libs


def add_library(rem_days, libras, order, lib_index, sc_books):
    rem_days -= libras[lib_index]["signup_days"]
    rem_days += 1
    n = rem_days * libras[lib_index]["per_day"]
    index = 0
    scan_completed_books = list()

    libras[lib_index]["books"].sort(key=lambda x: books_scores[int(x)], reverse=True)
    while n > 0 and index < len(libras[lib_index]["books"]) and not len(libras[lib_index]["books"]) == 0:
        book = libras[lib_index]["books"][index]
        scan_completed_books.append(book)
        n -= 1
        index += 1

    sc_books |= set(scan_completed_books)
    libras[lib_index]["scanned_books"] = scan_completed_books
    if not len(libras[lib_index]["scanned_books"]) == 0:
        order.append(libras[lib_index].copy())
    libras.pop(lib_index)
    return rem_days, libras, order, sc_books


def cost(order):
    total_score = 0
    for lib in order:
        for x in lib["scanned_books"]:
            total_score += books_scores[int(x)]
    return total_score


def choose(rem_days, libras, order, lib1, lib2, sc_books):
    temp_days = rem_days
    temp_libras = libras.copy()
    temp_order = order.copy()
    temp_sc_books = sc_books.copy()

    temp_days, temp_libras, temp_order, temp_sc_books = \
        add_library(temp_days, temp_libras, temp_order, lib1, temp_sc_books)
    temp_libras = update_priorities(temp_days, temp_libras, temp_sc_books.copy())

    next_best = max(temp_libras.keys(), key=lambda x: temp_libras[x]["priority"])
    temp_days, temp_libras, temp_order, temp_sc_books = \
        add_library(temp_days, temp_libras, temp_order, next_best, temp_sc_books)
    score1 = cost(temp_order)

    temp_days = rem_days
    temp_libras = libras.copy()
    temp_libras.pop(lib1)
    temp_order = order.copy()
    temp_sc_books = sc_books.copy()

    if len(temp_libras) > 2:
        temp_days, temp_libras, temp_order, temp_sc_books = \
            add_library(temp_days, temp_libras, temp_order, lib2, temp_sc_books)
        temp_libras = update_priorities(temp_days, temp_libras, temp_sc_books.copy())

        next_best = max(temp_libras.keys(), key=lambda x: temp_libras[x]["priority"])
        temp_days, temp_libras, temp_order, temp_sc_books = \
            add_library(temp_days, temp_libras, temp_order, next_best, temp_sc_books)
        score2 = cost(temp_order)
    else:
        score2 = 0

    if score1 > score2:
        return lib1
    else:
        return lib2


total_books, total_libraries, total_days, books_scores, libraries = get_input("f.txt")
library_order = []
scanned_books = set()
scanned_libraries = set()
remaining_days = total_days

for i in range(total_libraries):
    libraries[str(i)]["books"].sort(key=lambda x: books_scores[int(x)], reverse=True)

while remaining_days > 0 and not len(libraries) == 0:
    libraries = update_priorities(remaining_days, libraries, scanned_books)
    max_index1 = max(libraries.keys(), key=lambda x: libraries[x]["priority"])
    libraries_copy = libraries.copy()
    libraries_copy.pop(max_index1)
    if len(libraries_copy) > 2:
        max_index2 = max(libraries_copy.keys(), key=lambda x: libraries_copy[x]["priority"])
        best_index = \
            choose(remaining_days, libraries, library_order, max_index1, max_index2, scanned_books)
    else:
        best_index = max_index1
    if best_index in scanned_libraries:
        libraries.pop(best_index)
        continue
    remaining_days, libraries, library_order, scanned_books = \
        add_library(remaining_days, libraries, library_order, best_index, scanned_books)
    scanned_libraries.add(best_index)
    print("Remained ", remaining_days, " days")

print(cost(library_order))
write_output("f_out.txt")
