from random import shuffle
from typing import List, Tuple

# zalozenie TIME zawiera MINIMALNY CZAS, TIME_CONST to akceptowalny dodatkowy czas
def calculate_cost(t, start, end, time, hours, matrix):
    n = len(t)

    starts = [0 for _ in range(n)]
    cost = max(0, hours[t[0]][0]-start)
    current_time = max(hours[t[0]][0], start) + time[0]
    starts[0] = current_time - time[0]

    for i in range(1, n):

        cost += matrix[t[i-1]][t[i]] #przejazd
        current_time += matrix[t[i-1]][t[i]]

        # czekac trzeba
        if current_time+1 < hours[t[i]][0]:
            cost += hours[t[i]][0]-(current_time+1)
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

    while sum(time) > end_hour-start_hour:
        time.pop()
        hours.pop()

    n = len(hours)
    if n == 0: return [], []
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
            best = a.copy(), starts.copy()

            min_cost = cost

    if min_cost == float("inf") or any(((x[1] != 0) and (x[1] < start_hour)) for x in hours):
        hours.pop()
        time.pop()
        return find_path(start_hour, end_hour, time, hours, matrix, start_point)
    return best

if __name__ == "__main__":
    time = [1, 0.5, 1, 0.5, 0.25, 1, 0.25, 0.5, 0.5, 2, 0.5, 0.5,]
    hours = [ (0,0), (0,0), (0,0), (12,14), (0,0), (18,20), (16,20), (0,0), (0,0), (6,13), (0,0), (0,0), ]
    matrix = [
        [0.0, 0.39805833333333335, 0.6568222222222222, 0.7662444444444444, 0.3433333333333333, 0.5050277777777777, 0.42512222222222223]
        [0.39805833333333335, 0.0, 0.6084194444444444, 0.9945861111111112, 0.38668888888888886, 0.6284805555555556, 0.5802777777777778]
        [0.6568222222222222, 0.6084194444444444, 0.0, 0.6121583333333334, 0.3702444444444445, 0.3985583333333333, 0.4168222222222222]
        [0.7662444444444444, 0.9945861111111112, 0.6121583333333334, 0.0, 0.62695, 0.3763972222222222, 0.4569805555555556]
        [0.3433333333333333, 0.38668888888888886, 0.3702444444444445, 0.62695, 0.0, 0.26084166666666664, 0.19358888888888887]
        [0.5050277777777777, 0.6284805555555556, 0.3985583333333333, 0.3763972222222222, 0.26084166666666664, 0.0, 0.09083055555555555]
        [0.42512222222222223, 0.5802777777777778, 0.4168222222222222, 0.4569805555555556, 0.19358888888888887, 0.09083055555555555, 0.0]

    ]
    
    print("6-19", find_path(6, 19, time, hours, matrix))
    print("6-14", find_path(6, 14, time, hours, matrix))
    print("6-12", find_path(6, 12, time, hours, matrix))
    print("6-9", find_path(6, 9, time, hours, matrix))
    print("6-7", find_path(6, 7, time, hours, matrix))



