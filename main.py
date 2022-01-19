import csv

def comparing_lists(num, str_in_file):
    answer = ans_dict[ans_keys[num]]
    if answer == '' or str_in_file =='Unknown': percent = 0
    else:
        ans_list = answer.split(', ')
        str_in_file.replace('"', '')
        str_list = str_in_file.split(', ')
        quantity = 0

        for i in range(len(ans_list)):
            for j in range(len(str_list)):
                if ans_list[i] == str_list[j]:
                    quantity += 1
        percent = 100 * quantity / len(str_list)
    return percent

def episodes (num, str_in_file):
    percent = 0
    answer = ans_dict[ans_keys[num]]
    if answer == '' or str_in_file == 'Unknown' : percent = 0
    else:
        if answer == 'многосерийное':
            if int(str_in_file) > 1 : percent = 100
            else : percent = 0
        else :
            if int(str_in_file) == 1 : percent = 100
            else : percent = 0
    return percent

def finished (num, str_in_file):
    percent = 0
    answer = ans_dict[ans_keys[num]]
    if answer == '' or str_in_file =='Unknown': percent = 0
    else:
        if answer == 'да':
            if  str_in_file == 'True' : percent = 100
            else : percent = 0
        else :
            if str_in_file == 'False' : percent = 100
            else : percent = 0
    return percent

def years (num, StartYear,EndYear):
    percent = 0
    answer = ans_dict[ans_keys[num]]
    if answer == '' or StartYear =='Unknown' or EndYear=='Unknown': percent = 0
    else:
        ans_list = answer.split(', ')
        inaccuracy = abs(int(StartYear)-int(ans_list[0])) + abs(int(EndYear)-int(ans_list[1]))
        if inaccuracy <= 20 : percent = 100-inaccuracy*5
        else : percent = 0
    return percent

def rating (num, str_in_file):
    percent = 0
    if emptiness == 7: answer = 5
    else: answer = ans_dict[ans_keys[num]]
    if answer == '' or str_in_file =='Unknown': percent = 0
    else:
        if int(answer) <= int(str_in_file) :
            percent = 100
        else: percent = 100-(int(answer)-int(str_in_file))*10
    return percent

def questions(n):
    if n == 0:
        print('Назовите интересующие жанры через запятую. Enter - если вам не важен жанр.')
    elif n == 1:
        print('Назовите интересующие студии через запятую. Enter - если вам не важна студия.')
    elif n == 2:
        print('Назовите интересующие типы аниме через запятую. Например: DVD, Movie, Music, OVA, TV, Web, Other. Enter - если тип вам не важен.')
    elif n == 3:
        print('Вас интересует многосерийное аниме или полнометражное? Enter - если вам не важно.')
    elif n == 4:
        print('Какой  рейтинг вас интересует? (Введите число от 0 до 5). Enter - если вам не важна длительность.')
    elif n == 5:
        print('Вас интересует завершенный проект или нет? Ответьте да или нет. Enter - если вам не важно.')
    elif n == 6:
        print('Укажите интересуещие вас года выпуска в формате "начало, конец".Например (1990, 2005) . Enter - если вам не важно.')
    else:
        print('<<< Ошибка >>>')


ans_dict = dict.fromkeys(['Tags', 'Studios', 'Type', 'Episodes', 'Rating Score', 'Finished', 'Years'])
ans_keys = list(iter(ans_dict))
emptiness = 0
for num in range(len(ans_keys)):
    questions(num)
    answer = str(input())
    if answer == '': emptiness+=1
    ans_dict[ans_keys[num]] = answer

with open('anime.csv', 'r', encoding='utf8') as file:
    anime_reader = csv.DictReader(file)
    name_list = [ '',  '',  '',  '',  '',  '',  '',  '',  '', '']
    max_res_list = [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0]

    for line in anime_reader:
        result_perp=0
        for i in range(0,3):
            result_perp += comparing_lists(i, line[ans_keys[i]]) # tags,studios,tipes
        result_perp += episodes(3, line[ans_keys[3]])
        result_perp += rating(4, line[ans_keys[3]])
        result_perp += finished(5, line[ans_keys[5]])
        result_perp += years(6, line['StartYear'], line['EndYear'])
        if result_perp > min(max_res_list):
            lst_num = list(enumerate(max_res_list, 0))
            t_min = min(lst_num, key=lambda i: i[1])
            max_res_list[t_min[0]]=result_perp
            name_list[t_min[0]] = line['Name']
            
    all_res = [(max_res_list[i], name_list[i]) for i in range(len(name_list))]
    all_res.sort(reverse=True)
    print("Вы можете посмотреть список 10 подходящих вам аниме в файле Top 10")
    with open('Top 10.txt', 'w', encoding='utf-8') as file:
        num=0
        for i in all_res:
            num+=1
            file.write(str(num) + ')' + i[1]+ '\n')
