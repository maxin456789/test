




def histogram(data):
    stat_data = {}
    for letters in tuple(data):
        if letters not in stat_data.keys():
            stat_data[letters] = int(1)
        else:
            stat_data[letters] = stat_data[letters] + 1
    max_value = sorted(stat_data.values())[-1]
    i = max_value
    while i > 0:
        mess_for_print = ''
        for keys in sorted(stat_data.keys()):
            if stat_data[keys] >= i:
                mess_for_print = mess_for_print + '|'
            else:
                mess_for_print = mess_for_print + ' '
        i = i - 1
        print(mess_for_print)
    last_mes = ''
    for keys in sorted(stat_data.keys()):
        last_mes = f'{last_mes}{keys}'
    return(last_mes)





print(histogram("ececceaebdadaeae"))
print(histogram("dbcaabdc"))
print(histogram("aaabbc"))
print(histogram("a b a!b"))
print(histogram("abcde"))
print(histogram("aaaaaa"))