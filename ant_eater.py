import keyboard
import time
import os, random


difficulty = input("Введи сложность (baby, normal, hard, insane):")

Go = input('Введи "go" для запуска игры ("?" для подсказки):')

global Game
Game = True
Ant_Eater, Ant_Hill, Ant, Grass, Stone = '☺','▲','8','░', '█'

size = 10

Go = input('Введи "go" для запуска игры:') #- Введен запуск игры через ключ "go"

global Game
Game = True
Ant_Eater, Ant_Hill, Ant, Grass, Stone = '☺','▲','8','░', '█' #- изменена иконка муравья с "¤" на "8".

size = 10 #- изменен базовый размер поля, для лучшего восприятия игроком.

X = Y = size//2

Field =[]
for i in range(size):
    Field.append([])
    for j in range(size):
        Field[i].append(Grass)

Field[Y][X] = Ant_Eater
print(Field)
for i in range(random.randint(5,10)):
    rnd_X = random.randint(0,size-1)
    rnd_Y = random.randint(0,size-1)
    Field[rnd_Y][rnd_X] = Stone

anthills = []
for i in range(random.randint(2,4)):
    anthills.append([])
    rnd_X = random.randint(3,size-3)
    rnd_Y = random.randint(3,size-3)
    rnd_N = random.randint(3,10)
    anthills[i].append([rnd_X,rnd_Y,rnd_N])
    Field[rnd_Y][rnd_X] = Ant_Hill
if Go == "go":
    del Go
    def draw():
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(size):
            for j in range(size):
                print(Field[i][j], end="")
            print()
        global eaten
        global gone
        ant_count = 0
        for hill in anthills:
            ant_count += hill[0][2]
        if ant_count<1:
            print("-----------Игра окончена-----------\nМуравьев в муравейниках больше не осталось (на поле они не такие вкусные).\n Игра завершена. Ваш счет: ", eaten - gone,
                  "\n(кол-во съеденых муравьев, отнять кол-во сбежавших)")
            exit()

        print("Съедено:", eaten,"|", " Убежало: ", gone,"|", "На поле: ", len(ants),"|", "Осталось: ", ant_count, "|")
    def exit1():
        global Game
        Game = False

    def can_move(current_x, current_y, delta_x, delta_y):
        x = current_x + delta_x
        y = current_y + delta_y
        if (x<0) or (y<0) or (x>=size) or (y>=size):
            return False
        if (Field[y][x] == Stone) or (Field[y][x] == Ant_Hill) or (Field[y][x] == Ant_Eater):
            return False
        return True
    def move_ant_eater(current_x, current_y,delta_x, delta_y):
        Field[current_y][current_x] = Grass
        global X
        global Y
        X= current_x + delta_x
        Y= current_y + delta_y
        if Field[Y][X] == Ant:
            global eaten
            eaten += 1
            try:
                ants.remove([X,Y])
            except:
                pass
        Field[Y][X] = Ant_Eater

    def move_left():
        if can_move(X,Y,-1,0):
            move_ant_eater(X,Y,-1, 0)
            draw()

    def move_right():
        if can_move(X,Y,1,0):
            move_ant_eater(X,Y,1, 0)
            draw()
    def move_up():
        if can_move(X,Y,0,-1):
            move_ant_eater(X,Y,0, -1)
            draw()
    def move_down():
        if can_move(X,Y,0,1):
            move_ant_eater(X,Y,0, 1)
            draw()
    last_t = time.time()
    keyboard.add_hotkey('left', move_left)
    keyboard.add_hotkey('right', move_right)
    keyboard.add_hotkey('up', move_up)
    keyboard.add_hotkey('down', move_down)
    keyboard.add_hotkey('esc', exit1)


    ants = []

    def spawn(hill):
        rnd_X = random.randint(-1, 1)
        rnd_Y = random.randint(-1,1)
        x = hill[0][0]
        y = hill[0][1]
        n = hill[0][2]
        if can_move(x,y,rnd_X,rnd_Y) and n>0:
            ants.append([x+rnd_X,y+rnd_Y])
            Field[y+rnd_Y][x+rnd_X] = Ant
            return True
        return False
    def move_ants(ants):
        for ant in ants:
            x = ant[0]
            y = ant[1]
            rnd_X = random.randint(-1, 1)
            rnd_Y = random.randint(-1,1)
            if can_move(x,y,rnd_X,rnd_Y):
                ant = [x+rnd_X,y+rnd_Y]

                Field[y][x] = Grass
                if ((x+rnd_X == 0) or (x+rnd_X == size-1) or
                        (y+rnd_Y == 0) or (y+rnd_Y == size-1)):
                    global gone
                    gone += 1
                    try:
                        ants.remove([x+rnd_X,y+rnd_Y])
                    except:
                        pass
                else:
                    Field[y+rnd_Y][x+rnd_X] = Ant

    eaten=0
    gone=0
    if difficulty == "normal":
        while Game:
            t = time.time()
            if t-last_t>3:
                move_ants(ants)
                rnd_hill = random.randint(0,len(anthills)-1)
                if spawn(anthills[rnd_hill]):
                    anthills[rnd_hill][0][2] -= 1
                draw()

                last_t = t
    elif difficulty == "baby":
        while Game:
            t = time.time()
            if t - last_t > 5:
                move_ants(ants)
                rnd_hill = random.randint(0, len(anthills) - 1)
                if spawn(anthills[rnd_hill]):
                    anthills[rnd_hill][0][2] -= 1
                draw()

                last_t = t
    elif difficulty == "hard":
        while Game:
            t = time.time()
            if t - last_t > 2:
                move_ants(ants)
                rnd_hill = random.randint(0, len(anthills) - 1)
                if spawn(anthills[rnd_hill]):
                    anthills[rnd_hill][0][2] -= 1
                draw()

                last_t = t
    elif difficulty == "insane":
        while Game:
            t = time.time()
            if t - last_t > 1:
                move_ants(ants)
                rnd_hill = random.randint(0, len(anthills) - 1)
                if spawn(anthills[rnd_hill]):
                    anthills[rnd_hill][0][2] -= 1
                draw()

                last_t = t


elif Go == "?":
    print("----------Игра «Ловкий муравьед».----------\n Главный герой – голодный, но очень ловкий муравьед"
          " бегает по двумерному полю от одного муравейника к другому\n и вылавливает убегающих за границу экрана муравьёв.\n"
          "☺ — главный герой, может передигаться по игровому полю (стрелочки на клавиатуре)\n и поедать муравьев (становясь на одну клетку с ними).\n"
          "8 — муравей, может случайно перемещаться по игровому полю (скорость зависит от сложности).\n"
          "Может выбежать за экран.\n"
          "▲ — муравейник, из него появляются муравьи (в случайном количестве).\n"
          "░ — клетка игрового поля, по которой могут передвигаться и муравьи, и игрок.\n"
          "█ — недоступная клетка игрового поля, по которой нельзя передвигаться.\n"
          "------------------------------------------------------------------"
          '\nDOGGY — если при запуске игры вместо "go" ввести "DOGGY",\n символ игрока изменится на "@"'
          '\nRevenge mode — если при запуске игры вместо "go" ввести "Revenge mode",\n символ игрока изменится на "8", а символ муравья на "☺"\nДа начнется месть!'

        )
    input()

elif Go == "Revenge mode":
    Ant_Eater = "8"
    Ant = "☺"

if Go == "go": #- Введен запуск игры через ключ "go"

    def draw():
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(size):
            for j in range(size):
                print(Field[i][j], end="")
            print()

        global eaten
        global gone
        ant_count = 0
        for hill in anthills:
            ant_count += hill[0][2]
        if ant_count<1:
            print("||-----------Месть удалась-----------||\nМуравьедов в гнездах больше не осталось (на поле они не так интересны).\n Игра завершена. Ваш счет: ", eaten - gone,
                  "\n(кол-во убитых муравьедов, отнять кол-во сбежавших)")
            exit()

        print("Убито:", eaten,"|", " Убежало: ", gone,"|", "На поле: ", len(ants),"|", "Осталось: ", ant_count, "|")



    def exit1():
        global Game
        Game = False

    def can_move(current_x, current_y, delta_x, delta_y):
        x = current_x + delta_x
        y = current_y + delta_y
        if (x<0) or (y<0) or (x>=size) or (y>=size):
            return False
        if (Field[y][x] == Stone) or (Field[y][x] == Ant_Hill) or (Field[y][x] == Ant_Eater):
            return False
        return True
    def move_ant_eater(current_x, current_y,delta_x, delta_y):
        Field[current_y][current_x] = Grass
        global X
        global Y
        X= current_x + delta_x
        Y= current_y + delta_y

        if Field[Y][X] == Ant:
            global eaten
            eaten += 1
            try:
                ants.remove([X,Y])
            except:
                pass

        Field[Y][X] = Ant_Eater
        #print("moving", X, Y)
    def move_left():
        if can_move(X,Y,-1,0):
            move_ant_eater(X,Y,-1, 0)
            draw()

    #    else:
    #        print("cannot_move",X,Y,-1,0)

#       else:
#           print("cannot_move",X,Y,-1,0)

    def move_right():
        if can_move(X,Y,1,0):
            move_ant_eater(X,Y,1, 0)
            draw()
    def move_up():
        if can_move(X,Y,0,-1):
            move_ant_eater(X,Y,0, -1)
            draw()
    def move_down():
        if can_move(X,Y,0,1):
            move_ant_eater(X,Y,0, 1)
            draw()
    last_t = time.time()
    keyboard.add_hotkey('left', move_left)
    keyboard.add_hotkey('right', move_right)
    keyboard.add_hotkey('up', move_up)
    keyboard.add_hotkey('down', move_down)
    keyboard.add_hotkey('esc', exit1)


    ants = []

    def spawn(hill):
        rnd_X = random.randint(-1, 1)
        rnd_Y = random.randint(-1,1)
        x = hill[0][0]
        y = hill[0][1]
        n = hill[0][2]
        if can_move(x,y,rnd_X,rnd_Y) and n>0:
            ants.append([x+rnd_X,y+rnd_Y])
            Field[y+rnd_Y][x+rnd_X] = Ant
            return True
        return False
    def move_ants(ants):
        for ant in ants:
            x = ant[0]
            y = ant[1]
            rnd_X = random.randint(-1, 1)
            rnd_Y = random.randint(-1,1)
            if can_move(x,y,rnd_X,rnd_Y):
                ant = [x+rnd_X,y+rnd_Y]

                Field[y][x] = Grass
                if ((x+rnd_X == 0) or (x+rnd_X == size-1) or
                        (y+rnd_Y == 0) or (y+rnd_Y == size-1)):
                    global gone
                    gone += 1
                    try:
                        ants.remove([x+rnd_X,y+rnd_Y])
                    except:
                        pass
                else:
                    Field[y+rnd_Y][x+rnd_X] = Ant

    eaten=0
    gone=0
    if difficulty == "normal":
        while Game:
            t = time.time()
            if t-last_t>3:
                move_ants(ants)
                rnd_hill = random.randint(0,len(anthills)-1)
                if spawn(anthills[rnd_hill]):
                    anthills[rnd_hill][0][2] -= 1
                draw()
                #print(t)
                last_t = t
    elif difficulty == "baby":
        while Game:
            t = time.time()
            if t - last_t > 5:
                move_ants(ants)
                rnd_hill = random.randint(0, len(anthills) - 1)
                if spawn(anthills[rnd_hill]):
                    anthills[rnd_hill][0][2] -= 1
                draw()
                # print(t)
                last_t = t
    elif difficulty == "hard":
        while Game:
            t = time.time()
            if t - last_t > 2:
                move_ants(ants)
                rnd_hill = random.randint(0, len(anthills) - 1)
                if spawn(anthills[rnd_hill]):
                    anthills[rnd_hill][0][2] -= 1
                draw()
                # print(t)
                last_t = t
    elif difficulty == "insane":
        while Game:
            t = time.time()
            if t - last_t > 1:
                move_ants(ants)
                rnd_hill = random.randint(0, len(anthills) - 1)
                if spawn(anthills[rnd_hill]):
                    anthills[rnd_hill][0][2] -= 1
                draw()
                # print(t)
                last_t = t

else:
    print("|--------Неизвестный ключ--------|\n"
          "Попробуйте еще раз, или убедитесь, что у вас\n стоит нужная раскладка клавиатуры.\n"
          "Допустимые ключи: 'go', 'DOGGY', 'Revenge mode'\n"
          "Их свойства можно прочитать в подсказке при запуске игры.")
try:
    keyboard.unhook_all_hotkeys()
except:
    pass

    while Game:
        t= time.time()
        if t-last_t>2:
            draw()
            print(t)
            last_t = t

keyboard.unhook_all_hotkeys()

