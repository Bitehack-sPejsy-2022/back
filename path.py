from random import shuffle

time = [1, 0.5, 1, 0.5, 0.25, 1, 0.25, 0.5, 0.5, 2, 0.5, 0.5,]
hours = [ (0,0), (0,0), (0,0), (12,14), (0,0), (18,20), (16,20), (0,0), (0,0), (6,13), (0,0), (0,0), ]
matrix = [
[0.028215201572564512, 0.00972219130655745, 0.012263459400873903, 0.006336571490857871, 0.012403906143245528, 0.0010364334115123932, 0.12841389597498962, 0.019090682802184802, 0.21331752276135316, 0.07759912227647964, 0.08853188194612001, 0.1431099087648065] ,
[0.08511659477757079, 0.030142730564070942, 0.05742695701378757, 0.07237183362840655, 0.03621962802961166, 0.054433286602381684, 0.30291699255015525, 0.255866982718941, 0.22831409040961614, 0.05271640987640762, 0.08202525393233394, 0.0002678681076829631] ,
[0.09882158738081698, 0.04154345455996116, 0.0012804042058667151, 0.012200358791944544, 0.1247372750104361, 0.004295354653591821, 0.08296865075572549, 0.3898798452289758, 0.05561542453678095, 0.01968833546442372, 0.21291386037543558, 0.1747502787118865] ,
[0.01783546794576085, 0.00033643537061927854, 0.022314781619385906, 0.02711088859891552, 0.04618113730595958, 0.10408856105266744, 0.021730010725055007, 0.41119545944843017, 0.01737474752958982, 0.019003375046781488, 0.02081830019881419, 0.002479168934700649] ,
[0.00034639946754136543, 0.04148549432446854, 0.0209270783308794, 0.001487443286484868, 0.03642559169340857, 0.00965297397816552, 0.06633342711875338, 0.007229474414232676, 0.06699742242844718, 0.038987958116659664, 0.0007226625569485956, 0.1252128188312404] ,
[0.04285170691712916, 0.07545163366893025, 0.013964741204177069, 0.016880815960574187, 0.0049765338827783305, 0.07787359888303155, 0.08579048553179881, 0.07880271886167714, 0.22830703248792084, 0.034261773459247614, 0.06431944014658883, 0.35480600247737487] ,
[0.010831055605260436, 0.024481189023031154, 0.0027955718738220717, 0.00802367041905385, 0.20175426111641462, 0.009450106554636526, 0.15881319133341537, 0.2761039544252855, 0.4413423393689317, 0.03366070381208576, 0.07014517405882979, 0.004119303077447668] ,
[0.08143707407945669, 0.07496708363403948, 0.00628148610483297, 0.18049903818344537, 0.02642127013904215, 0.035850794287875576, 0.017298009434909417, 0.08055357098676454, 0.10089640977731335, 0.027814726010544747, 0.007586191889505669, 0.14799543099602053] ,
[0.009265989236807605, 0.3967339205791295, 0.12188129259979642, 0.02500220606146281, 0.23783275082757624, 0.04477545595016394, 0.057626646359688796, 0.003359631095164431, 0.004205542365955704, 0.007050088879742387, 0.03918007360331546, 0.004682305869799872] ,
[0.00045116150820991295, 2.258518048452927e-05, 0.02032808780646924, 0.0017691081730095322, 0.011598703592887226, 0.03897783181941749, 0.0033386013756369483, 0.009594881050453776, 0.06515850222604565, 0.42432593961077925, 0.028546594173109258, 0.008378058612701385] ,
[0.7233330740205592, 0.00041045898664082074, 0.003435940868359368, 0.0392584604184839, 4.477927084236159e-05, 1.0342183757193517e-05, 0.19938199136632487, 0.008614957022690833, 0.004107759100888593, 0.23852099608661773, 0.006248054445340156, 0.07641545696922095] ,
[0.032596568220180255, 0.0006511130966054608, 0.11454514196402023, 0.015289198781628262, 0.004227995755128523, 0.00026179347409894534, 0.3338834239168284, 0.1714041692322827, 0.14840122949063705, 0.07041342117293002, 0.0002685057571269538, 0.011426452716326021] ,
]

# zalozenie TIME zawiera MINIMALNY CZAS, TIME_CONST to akceptowalny dodatkowy czas
def calculate_cost(t, start, end, time, hours, matrix):
    n = len(t)
    starts = [0 for _ in range(n)]
    cost = max(0, hours[t[0]][0]-start)
    current_time = max(hours[t[0]][0], start)
    starts[0] = current_time
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

def find_path(start_hour, end_hour, time, hours, matrix, start_point = None):
    while sum(time) > end_hour-start_hour:
        time.pop()
        hours.pop()
    n = len(hours)
    if n == 0: return [], []
    ITER = 100000
    a = [i for i in range(n)]
    best = [], []
    min_cost = float("inf")
    for _ in range(ITER):
        shuffle(a)
        if start_point is not None:
            i = a.index(start_point)
            a[0], a[i] = a[i], a[0]
        cost, starts = calculate_cost(a, start_hour, end_hour, time, hours, matrix)
        if cost < min_cost:
            best = a, starts
            min_cost = cost
    if min_cost == float("inf") or any(((x[1] != 0) and (x[1] < start_hour)) for x in hours):
        hours.pop()
        time.pop()
        return find_path(start_hour, end_hour, time, hours, matrix, start_point)
    return best

if __name__ == "__main__":
    print("6-19", find_path(6, 19, time, hours, matrix))
    print("6-14", find_path(6, 14, time, hours, matrix))
    print("6-12", find_path(6, 12, time, hours, matrix))
    print("6-9", find_path(6, 9, time, hours, matrix))
    print("6-7", find_path(6, 7, time, hours, matrix))


