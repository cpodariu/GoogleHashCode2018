import random
from collections import deque

input = "e_high_bonus.in"
output = "result_e.out"


class Ride:
    def __init__(self, string, index):
        self.index = index
        string = deque(string.split(" "))
        self.start_row = int(string.popleft())
        self.start_column = int(string.popleft())
        self.end_row = int(string.popleft())
        self.end_column = int(string.popleft())
        self.start_time = int(string.popleft())
        self.end_time = int(string.popleft())


class Car:
    def __init__(self):
        self.is_first = True
        self.row = 0
        self.column = 0
        self.destination_row = 0
        self.destination_column = 0
        self.steps_left = 0
        self.current_ride = None
        self.done_rides = []
        self.path = []


file = open(input)
file_string = file.read()

file_string = file_string.split("\n")
file_string_deque = deque(file_string)

first_line = deque(file_string_deque.popleft().split(" "))

rows = int(first_line.popleft())
columns = int(first_line.popleft())
vehicles = int(first_line.popleft())
rides = int(first_line.popleft())
bonus = int(first_line.popleft())
number_of_steps = int(first_line.popleft())
current_step = 0

rides_set = {}
rides_index = 0
for i in file_string_deque:
    if i == "":
        break
    r = Ride(i, rides_index)
    rides_index += 1
    rides_set[r.start_row, r.start_column] = r

car_set = []
for i in range(vehicles):
    car_set.append(Car())


def get_distance(a, b, x, y):
    return abs(a - x) + abs(b - y)


def get_points(car, ride, time):
    current_bonus = 0
    cost = 0
    cost = cost + get_distance(car.row, car.column, ride.start_row, ride.start_column)
    points = get_distance(ride.start_row, ride.start_column, ride.end_row, ride.end_column)
    if cost + time < ride.start_time:
        current_bonus += bonus
    if cost + time > ride.end_time:
        return 0, 1
    cost += points
    if cost + time == ride.start_time:
        current_bonus += bonus
    points += current_bonus
    return points, cost


done_rides = []



while current_step < number_of_steps:
    if current_step%100 == 0:
        print(current_step)
    for i in car_set:
        if i.is_first:
            while i.current_ride is None:
                ride = random.choice(list(rides_set.values()))
                v, c = get_points(i, ride, 0)
                if c < number_of_steps:
                    i.is_first = False
                    i.current_ride = ride
                    i.destination_row = ride.end_row
                    i.destination_column = ride.end_column
                    i.steps_left = c
                    rides_set.pop((ride.start_row, ride.start_column))
        else:
            if i.steps_left == 0:
                if i.current_ride is not None:
                    done_rides.append(i.current_ride)
                    i.done_rides.append(i.current_ride)
                    i.row = i.destination_row
                    i.column = i.destination_column
                    i.current_ride = None

                best_ride = None
                best_ride_efficiency = -1
                best_ride_cost = None
                for ride in rides_set.values():
                    # print('a')
                    result = get_points(i, ride, current_step)

                    current_points = result[0]
                    current_cost = result[1]
                    # print('b')
                    if current_points/current_cost > best_ride_efficiency:
                        best_ride = ride
                        best_ride_efficiency = current_points/current_cost
                        best_ride_cost = current_cost
                if best_ride is not None:
                    i.current_ride = rides_set.pop((best_ride.start_row, best_ride.start_column))
                    i.destination_row = best_ride.end_row
                    i.destination_column = best_ride.end_column
                    i.steps_left = best_ride_cost

    for decrease_cars_i in car_set:
        decrease_cars_i.steps_left -= 1
    if current_step%1000 == 0:
        rides_set = {k: v for k,v in rides_set.items() if v.end_time > current_step + get_distance(v.start_row, v.start_column, v.end_row, v.end_column)}

    current_step += 1

out_file = open(output, "w")
for i in car_set:
    out_file.write(str(len(i.done_rides)) + " ")
    for j in i.done_rides:
        out_file.write(str(j.index) + " ")
    out_file.write("\n")