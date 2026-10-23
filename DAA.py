from bisect import bisect_left, bisect_right

RADIUS = 500
INF = float("inf")


def build_intervals(houses, transmitters, radius=RADIUS):
    # for each transmitter find which houses it covers, as [L, R] (1-indexed)
    intervals = []
    for t in transmitters:
        L = bisect_left(houses, t - radius) + 1
        R = bisect_right(houses, t + radius)
        if L <= R:
            intervals.append((R, L, R - L + 1, t))
    intervals.sort()  # sort by right endpoint
    return intervals


def optimal_transmitters(houses, transmitters, radius=RADIUS):
    m = len(houses)
    if m == 0:
        return 0, []

    houses = sorted(houses)
    intervals = build_intervals(houses, transmitters, radius)
    n = len(intervals)
    if n == 0:
        return None

    # index 0 is the sentinel (R = 0, cost = 0)
    R = [0] + [iv[0] for iv in intervals]
    L = [0] + [iv[1] for iv in intervals]
    W = [0] + [iv[2] for iv in intervals]

    dp = [INF] * (n + 1)
    pred = [-1] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        for j in range(i):
            # j can come before i if there is no gap and R_j < R_i
            if L[i] - 1 <= R[j] < R[i]:
                if dp[j] + W[i] < dp[i]:
                    dp[i] = dp[j] + W[i]
                    pred[i] = j

    # pick the best interval that reaches the last house
    best = -1
    for i in range(1, n + 1):
        if R[i] == m and (best == -1 or dp[i] < dp[best]):
            best = i

    if best == -1 or dp[best] == INF:
        return None

    # walk back through pred to get the chosen transmitters
    chosen = []
    cur = best
    while cur != 0:
        chosen.append(intervals[cur - 1][3])
        cur = pred[cur]
    chosen.reverse()

    # answer = total length - m
    return dp[best] - m, chosen


def read_numbers(prompt):
    while True:
        try:
            nums = []
            for tok in input(prompt).replace(",", " ").split():
                x = float(tok)
                nums.append(int(x) if x.is_integer() else x)
            return nums
        except ValueError:
            print("Please enter numbers only, separated by spaces.")


if __name__ == "__main__":
    print("Optimal Placement of Transmitters (radius = 500 m)")
    print("Enter positions in metres, separated by spaces or commas.\n")

    houses = read_numbers("House positions: ")
    transmitters = read_numbers("Candidate transmitters: ")

    result = optimal_transmitters(houses, transmitters)

    print()
    if result is None:
        print("Infeasible: some house cannot be covered.")
    else:
        answer, chosen = result
        print("Minimum multiply-covered houses:", answer)
        print("Transmitters to build at:", chosen)
