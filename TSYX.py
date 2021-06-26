import turtle
import math
import random
import time
import numpy
from matplotlib import pyplot as plt


class Ellipses(object):


    def __init__(self, dis_to_earth, angle):
        self.dis_to_earth = dis_to_earth
        self.timer = 10*dis_to_earth
        self.angle = math.radians(angle)
        self.fuel = 5*angle
        self.elipsa = turtle.Turtle()
        self.elipsa.shape("turtle")
        self.elipsa.penup()
        self.elipsa.fillcolor("white")
        self.elipsa.setposition((earth.xcor()+(math.cos(self.angle)*dis_to_earth)), (earth.ycor()+(math.sin(self.angle)*dis_to_earth)))
        self.y_coordinate = self.elipsa.ycor()
        self.x_coordinate = self.elipsa.xcor()
        self.ellipse_data = [self.dis_to_earth, self.angle]
        self.distance_to_mars = self.elipsa.distance(mars)

    def movement(self):
        self.elipsa.setposition((earth.xcor() + (math.cos(self.angle) * self.dis_to_earth)), (earth.ycor() + (math.sin(self.angle) * self.dis_to_earth)))

    def hide(self):
        self.elipsa.hideturtle()

    def clear(self):
        self.elipsa.clear()


def choose_values():
    distance = random.randint(244, 696)
    ang = random.randint(0, 360)
    any_orbit = Ellipses(distance, ang)
    return any_orbit


def define_fuel_and_time_after_ellipse(ellipse_object: Ellipses, taboo_or_not: int):
    global timer
    global fuel
    if taboo_or_not == 1:
        czas = timer + ellipse_object.timer
        paliwo = fuel - ellipse_object.fuel
        timer = czas
        fuel = paliwo
        travel_time.append(timer)
        travel_fuel.append(fuel)
    if taboo_or_not == 0:
        czas = timer + ellipse_object.timer
        timer = czas
        travel_time.append(timer)
        travel_fuel.append(fuel)
    print('Czas: {}'.format(timer))
    print('Paliwo: {}'.format(fuel))

def define_fuel_and_time_after_ellipse_mod(ellipse_object: Ellipses, taboo_or_not: int):
    global timer_mod
    global fuel_mod
    if taboo_or_not == 1:
        czas = timer_mod + ellipse_object.timer
        paliwo = fuel_mod - ellipse_object.fuel
        timer_mod = czas
        fuel_mod = paliwo
        travel_time_mod.append(timer_mod)
        travel_fuel_mod.append(fuel_mod)
    if taboo_or_not == 0:
        czas = timer_mod + ellipse_object.timer
        timer_mod = czas
        travel_time_mod.append(timer_mod)
        travel_fuel_mod.append(fuel_mod)
    print('Czas: {}'.format(timer_mod))
    print('Paliwo: {}'.format(fuel_mod))


def taboo_search():
    global podmieniacz
    podmieniacz = 0
    counter_list.append(choose_values())
    counter_list_mod_help.append(counter_list[-1])
    print('WYLOSOWANA WARTOSC: {}'.format(counter_list[-1].distance_to_mars))
    if len(counter_list) > 3:
        counter_list[0].hide()
        counter_list[0].clear()
        del(counter_list[0])
    tabu_list.append(counter_list[-1])
    if len(tabu_list) > 2:
        print("POCZATKOWA LISTA TABUU: [{},{},{}]".format(tabu_list[0].distance_to_mars, tabu_list[1].distance_to_mars, tabu_list[2].distance_to_mars))
    if len(tabu_list) > 1:
        for i in range(len(tabu_list)):
            if counter_list[-1].distance_to_mars > tabu_list[i].distance_to_mars:
                print('WYKORZYSTANIE LISTY TABU - PODMIANA')
                counter_list[-1] = tabu_list[i]
            if i == (len(tabu_list) - 1):
                print('NASTEPUJE PODMIANA WARTOSCI W LISCIE TABUU')
                tabu_list[-1] = counter_list[-1]
    if tabu_list[-1] in tabu_list[0:-1]:
        podmieniacz = 1
    print(podmieniacz)
    if podmieniacz == 1:
        define_fuel_and_time_after_ellipse(counter_list[-1], 0)
    if podmieniacz != 1:
        define_fuel_and_time_after_ellipse(counter_list[-1], 1)
    travel_list.append(counter_list[-1].distance_to_mars)
    # if len(counter_list) == 1:
    #     travel_fuel.append(counter_list[-1].fuel)
    #     travel_time.append(counter_list[-1].timer)
    # if len(counter_list) > 1:
    #     travel_fuel.append(counter_list[-1].fuel+travel_fuel[-1])
    #     travel_time.append(counter_list[-1].timer+travel_time[-1])
    counter_list[-1].movement()
    if len(tabu_list) <= 3:
        a = counter_list[-1].distance_to_mars
        print('Mars w odleglosci (opcja 1):')
        print(a)
        if a < minimal_distance:
            print('Trasa w 1 zlokalizowana ')
            if len(tabu_list) > 2:
                print("KONCOWA LISTA TABUU: [{},{},{}]".format(tabu_list[0].distance_to_mars, tabu_list[1].distance_to_mars, tabu_list[2].distance_to_mars))
            print('---------------------------------------------------')
            return 1
        if a >= minimal_distance:
            if len(tabu_list) > 2:
                print("KONCOWA LISTA TABUU: [{},{},{}]".format(tabu_list[0].distance_to_mars, tabu_list[1].distance_to_mars, tabu_list[2].distance_to_mars))
            print('---------------------------------------------------')
            return 0
    if len(tabu_list) > 3:
        a = counter_list[-1].distance_to_mars
        print('COUNTER LIST LENGTH CONTROL: {}'.format(len(counter_list)))
        print('Mars w odleglosci (opcja 2): {}'.format(a))
        del (tabu_list[0])
        print('TABOO LIST LENGTH CONTROL: {}'.format(len(tabu_list)))
        if a < minimal_distance:
            print('Trasa w 2 zlokalizowana')
            if len(tabu_list) > 2:
                print("KONCOWA LISTA TABUU: [{},{},{}]".format(tabu_list[0].distance_to_mars, tabu_list[1].distance_to_mars, tabu_list[2].distance_to_mars))
            print('---------------------------------------------------')
            return 1
        if a >= minimal_distance:
            if len(tabu_list) > 2:
                print("KONCOWA LISTA TABUU: [{},{},{}]".format(tabu_list[0].distance_to_mars, tabu_list[1].distance_to_mars, tabu_list[2].distance_to_mars))
            print('---------------------------------------------------')
            return 0


def taboo_search_mod():
    global podmieniacz1
    global element_counter
    podmieniacz1 = 0
    supreme = 0
    counter_list_mod.append(counter_list_mod_help[element_counter])
    element_counter = element_counter + 1
    print('WYLOSOWANA WARTOSC: {}'.format(counter_list_mod[-1].distance_to_mars))
    tabu_list_mod.append(counter_list_mod[-1])
    help_taboo = counter_list_mod[-1]
    if len(tabu_list_mod)-1 > 2:
        print("POCZATKOWA LISTA TABUU: [{},{},{}]".format(tabu_list_mod[0].distance_to_mars, tabu_list_mod[1].distance_to_mars, tabu_list_mod[2].distance_to_mars))
    if len(tabu_list_mod) > 1:
        for i in range(len(tabu_list_mod)-1):
            if counter_list_mod[-1].distance_to_mars > tabu_list_mod[i].distance_to_mars:
                print('WYKORZYSTANIE LISTY TABU - PODMIANA')
                counter_list_mod[-1] = tabu_list_mod[i]
                supreme = 1
            if i == (len(tabu_list_mod) - 2) and supreme == 0:
                print('NASTEPUJE PODMIANA WARTOSCI W LISCIE TABUU')
                tabu_list_mod[-1] = counter_list_mod[-1]
    if counter_list_mod[-1] == help_taboo:
        podmieniacz1 = 1
    print(podmieniacz1)
    if podmieniacz1 == 1:
        define_fuel_and_time_after_ellipse_mod(counter_list_mod[-1], 0)
    if podmieniacz1 != 1:
        define_fuel_and_time_after_ellipse_mod(counter_list_mod[-1], 1)
    travel_list_mod.append(counter_list_mod[-1].distance_to_mars)
    # if len(counter_list_mod) == 1:
    #     travel_fuel_mod.append(counter_list_mod[-1].fuel)
    #     travel_time_mod.append(counter_list_mod[-1].timer)
    # if len(counter_list_mod) > 1:
    #     travel_fuel_mod.append(counter_list_mod[-1].fuel+travel_fuel_mod[-1])
    #     travel_time_mod.append(counter_list_mod[-1].timer+travel_time_mod[-1])
    counter_list_mod[-1].movement()
    if len(tabu_list_mod) <= 3:
        a = counter_list_mod[-1].distance_to_mars
        print('Mars w odleglosci (opcja 1):')
        print(a)
        if a < minimal_distance:
            print('Trasa w 1 zlokalizowana ')
            if len(tabu_list_mod) > 2:
                print("KONCOWA LISTA TABUU: [{},{},{}]".format(tabu_list_mod[0].distance_to_mars, tabu_list_mod[1].distance_to_mars, tabu_list_mod[2].distance_to_mars))
            print('---------------------------------------------------')
            return 1
        if a >= minimal_distance:
            if len(tabu_list_mod) > 2:
                print("KONCOWA LISTA TABUU: [{},{},{}]".format(tabu_list_mod[0].distance_to_mars, tabu_list_mod[1].distance_to_mars, tabu_list_mod[2].distance_to_mars))
            print('---------------------------------------------------')
            return 0
    if len(tabu_list_mod) > 3:
        a = counter_list_mod[-1].distance_to_mars
        print('COUNTER LIST LENGTH CONTROL: {}'.format(len(counter_list_mod)))
        print('Mars w odleglosci (opcja 2): {}'.format(a))
        del (tabu_list_mod[0])
        print('TABOO LIST LENGTH CONTROL: {}'.format(len(tabu_list_mod)))
        if a < minimal_distance:
            print('Trasa w 2 zlokalizowana')
            if len(tabu_list_mod) > 2:
                print("KONCOWA LISTA TABUU: [{},{},{}]".format(tabu_list_mod[0].distance_to_mars, tabu_list_mod[1].distance_to_mars, tabu_list_mod[2].distance_to_mars))
            print('---------------------------------------------------')
            return 1
        if a >= minimal_distance:
            if len(tabu_list_mod) > 2:
                print("KONCOWA LISTA TABUU: [{},{},{}]".format(tabu_list_mod[0].distance_to_mars, tabu_list_mod[1].distance_to_mars, tabu_list_mod[2].distance_to_mars))
            print('---------------------------------------------------')
            return 0


def way_to_orbit(x,y, object, colors):
    object.dot(40, "yellow")
    object.color("white")
    object.fillcolor(colors)
    object.shape("circle")
    object.penup()
    object.setposition(x, y)
    object.pendown()


def ellipse(object1, object2):
    object1.speed(0)
    object2.speed(0)
    loop = True
    object2_xvel = 0
    object2_yvel = 1
    object1_xvel = 0
    object1_yvel = 1

    while loop:
        object2_xvel += math.cos(math.radians(object2.towards(0, 0))) * (1000 / (object2.xcor() ** 2 + object2.ycor() ** 2))
        object2_yvel += math.sin(math.radians(object2.towards(0, 0))) * (1000 / (object2.xcor() ** 2 + object2.ycor() ** 2))
        object2.setposition(object2.xcor() + object2_xvel, object2.ycor() + object2_yvel)

        object1_xvel += math.cos(math.radians(object1.towards(0, 0))) * (1000 / (object1.xcor() ** 2 + object1.ycor() ** 2))
        object1_yvel += math.sin(math.radians(object1.towards(0, 0))) * (1000 / (object1.xcor() ** 2 + object1.ycor() ** 2))
        object1.setposition(object1.xcor() + object1_xvel, object1.ycor() + object1_yvel)

        if taboo_search() == 1:
            print('END')
            print('CZAS: {}'.format(timer))
            print('PALIWO: {}'.format(fuel))
            print('MARS - ZIEMIA: {}'.format(earth.distance(mars)))
            print('TRASA : {}'.format(travel_list))
            print('WEKTOR PALIWA: {}'.format(travel_fuel))
            print('WEKTOR CZASU: {}'.format(travel_time))
            plt.title('FUEL CONSUMPTION IN TIME - MODIFIED TABOO')
            plt.xlabel('TIME')
            plt.ylabel('PALIWO')
            plt.plot(travel_time, travel_fuel)
            plt.show()
            break


def ellipse2(object1, object2):
    print('-------------------------------UWAGA! ROZPOCZETO DRUGA METODE!!!-----------------------------------')
    object1.speed(0)
    object2.speed(0)
    loop = True
    object2_xvel = 0
    object2_yvel = 1
    object1_xvel = 0
    object1_yvel = 1

    while loop:
        object2_xvel += math.cos(math.radians(object2.towards(0, 0))) * (1000 / (object2.xcor() ** 2 + object2.ycor() ** 2))
        object2_yvel += math.sin(math.radians(object2.towards(0, 0))) * (1000 / (object2.xcor() ** 2 + object2.ycor() ** 2))
        object2.setposition(object2.xcor() + object2_xvel, object2.ycor() + object2_yvel)

        object1_xvel += math.cos(math.radians(object1.towards(0, 0))) * (1000 / (object1.xcor() ** 2 + object1.ycor() ** 2))
        object1_yvel += math.sin(math.radians(object1.towards(0, 0))) * (1000 / (object1.xcor() ** 2 + object1.ycor() ** 2))
        object1.setposition(object1.xcor() + object1_xvel, object1.ycor() + object1_yvel)

        if taboo_search_mod() == 1:
            print('END')
            print('CZAS: {}'.format(timer))
            print('PALIWO: {}'.format(fuel))
            print('MARS - ZIEMIA: {}'.format(earth.distance(mars)))
            print('TRASA : {}'.format(travel_list_mod))
            print('WEKTOR PALIWA: {}'.format(travel_fuel_mod))
            print('WEKTOR CZASU: {}'.format(travel_time_mod))
            plt.title('FUEL CONSUMPTION IN TIME - ORIGINAL TABOO')
            plt.xlabel('TIME')
            plt.ylabel('PALIWO')
            plt.plot(travel_time_mod, travel_fuel_mod)
            plt.show()
            break

def tsyx_main():
    global earth,mars,travel_list_mod,travel_fuel_mod,travel_time_mod,travel_list,travel_fuel,travel_time,podmieniacz,podmieniacz1,element_counter,minimal_distance,tabu_list,counter_list,fuel,timer,fuel_mod,timer_mod,counter_list_mod,tabu_list_mod,counter_list_mod_help
    First_algorithm = []
    Second_algorithm = []

    for test in range(1):
        mars = turtle.Turtle()
        mars2 = turtle.Turtle()
        earth = turtle.Turtle()
        earth2 = turtle.Turtle()

        background = turtle.Screen()
        background.setup(1920, 1080)
        background.bgpic("space.gif")

        travel_list = []
        travel_list_mod = []
        travel_time = []
        travel_time_mod = []
        travel_fuel = []
        travel_fuel_mod = []
        podmieniacz = 0
        podmieniacz1 = 0
        element_counter = 0
        minimal_distance = 50
        tabu_list = []
        counter_list = []
        fuel = 1000000
        timer = 0
        fuel_mod = 1000000
        timer_mod = 0
        counter_list_mod = []
        tabu_list_mod = []
        counter_list_mod_help = []


        start = time.clock()
        way_to_orbit(620, 0, mars, "red")
        way_to_orbit(375, 0, earth, "blue")
        ellipse(mars, earth)
        end = time.clock()
        total = end - start
        First_algorithm.append(total)

        start = time.clock()
        way_to_orbit(620, 0, mars2, "red")
        way_to_orbit(375, 0, earth2, "blue")
        ellipse2(mars2, earth2)
        end = time.clock()
        total = end - start
        Second_algorithm.append(total)

        print(First_algorithm)
        print('.')
        print(Second_algorithm)
        background.clear()

    print('Avarage modified Taboo algorithm time: {}'.format(numpy.mean(First_algorithm)))
    print('Avarage proper Taboo algorithm time: {}'.format(numpy.mean(Second_algorithm)))


    turtle.done()





# print(Kamil_algorithm)
# print('.')
# print(Kadluczka_algorithm)
# turtle.done()
#
