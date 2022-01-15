from random import shuffle
from typing import List, Tuple

# zalozenie TIME zawiera MINIMALNY CZAS, TIME_CONST to akceptowalny dodatkowy czas
def calculate_cost(t, start, end, time, hours, matrix, TIME_CONST = 1):
    n = len(t)

    starts = [0 for _ in range(n)]
    cost = max(0, hours[t[0]][0]-start)
    current_time = max(hours[t[0]][0], start)
    starts[0] = current_time

    for i in range(1, n):
        cost += matrix[t[i-1]][t[i]] #przejazd
        current_time += matrix[t[i-1]][t[i]]

        # czekac trzeba
        if current_time+TIME_CONST < hours[t[i]][0]:
            cost += hours[t[i]][0]-(current_time+TIME_CONST)
            current_time = hours[t[i]][0]


        starts[i] = current_time


        current_time += time[t[i]]
        
        # czas sie skonczyl, pora umierac
        if current_time > min(end, hours[t[i]][1] if hours[t[i]][1] > 0 else float("inf")):

            return float("inf"), []
    return cost, starts

def find_path(
            start_hour: float, 
            end_hour: float, 
            time: List[float], 
            hours: List[Tuple[float, float]], 
            matrix: List[List[float]], 
            start_point = None
        ):

    n = len(hours)
    ITER = 100000
    a: List[int] = [i for i in range(n)]

    best = [], []
    min_cost = float("inf")

    for _ in range(ITER):
        shuffle(a)
        if start_point is not None:
            i = a.index(start_point)
            a[0], a[i] = a[i], a[0]

        starts: List[float]
        cost, starts = calculate_cost(a, start_hour, end_hour, time, hours, matrix)
        if cost < min_cost:
            best = a, starts

            min_cost = cost
    
    if min_cost == float("inf") and any(((x[1] != 0) and (x[1] < start_hour)) for x in hours):
        print("NIE DA SIE")

        return [], []
    return best

if __name__ == '__main__':
    for _ in range(5):
        print(find_path(6, 20, time, hours, matrix))



