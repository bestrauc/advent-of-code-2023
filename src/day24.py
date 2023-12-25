import sys

import numpy as np
from sympy import solve, symbols

import utils


def parse_input(line: str) -> tuple[tuple, tuple]:
    pos_str, velo_str = line.split(" @ ")
    return [
        list(map(int, pos_str.split(", "))),
        list(map(int, velo_str.split(", "))),
    ]


puzzle = utils.read_puzzle_input(sys.argv[1])
positions, velocities = zip(*map(parse_input, puzzle))
positions = np.stack(positions)
velocities = np.stack(velocities)


def intersection_time(i: int, j: int, dims: tuple[int, int]) -> np.ndarray | None:
    """Intersect lines by solving the set of equations via matrix inversion."""
    posdiff = positions[i, dims] - positions[j, dims]
    vmat = np.c_[velocities[j, dims], -velocities[i, dims]]
    try:
        t = np.linalg.inv(vmat) @ posdiff
    except np.linalg.LinAlgError:
        # If the lines don't intersect, we can't invert.
        return None

    return t[::-1]


# Part 1
rs, re = (200000000000000, 400000000000000)
ans = 0
dims = [0, 1]
for i in range(len(positions)):
    for j in range(i + 1, len(positions)):
        t = intersection_time(i, j, dims)
        if t is None:
            print(f"{i},{j} don't intersect.")
        else:
            ix, iy = positions[i, dims] + velocities[i, dims] * t[0]
            if (rs <= ix <= re) and (rs <= iy <= re) and t.min() >= 0:
                ans += 1

            print(f"{i},{j} intersect at ({ix:.2f}, {iy:.2f}), t={t[0]: .2f}")

print(ans)

# Part 2
# Here I tried some things - I first thought I would find two pairs of lines
# that run parallel in the input, which would constrain the feasible throws
# to the plane that these lines lie in. However, I unfortunately didn't find any.
#
# While thinking about how I could constrain the problem somehow (but being
# pretty hopeless about my geometric abilities), it occurred to me that that
# finding a line through any three trajectories should hopefully be enough to
# solve the problem, because that should only have one solution (as opposed to
# a throw through two points, which can vary its velocity to match any config).
#
# So I wrote down this on paper:
# s_m + v_m * t_1 = s_1 + v_1 * t_1
# s_m + v_m * t_2 = s_2 + v_2 * t_2
# s_m + v_m * t_3 = s_3 + v_3 * t_3
#
# Where (s_m + v_m *t) is the line whose start and velocity parameters we want
# to find. We want to find them such that they match the location of the hail
# at three positions at time points t1, t2 and t3, which we also have to find.
# This equation has 9 unknowns and 9 equations if you expand by coordinate.
#
# s_mx + vmx * t_1 = s_1x + v_1x * t_1
# s_my + vmy * t_1 = s_1y + v_1y * t_1
# s_mz + vmz * t_1 = s_1z + v_1z * t_1
# s_mx + vmx * t_2 = s_2x + v_2x * t_2
# s_my + vmy * t_2 = s_2y + v_2y * t_2
# s_mz + vmz * t_2 = s_2z + v_2z * t_2
# s_mx + vmx * t_3 = s_3x + v_3x * t_3
# s_my + vmy * t_3 = s_3y + v_3y * t_3
# s_mz + vmz * t_3 = s_3z + v_3z * t_3
#
# I just took the initial three hailstones and put them into the equations and
# then used a solver online to get the solution. Afterwards, I reimplemented it
# here in SymPy after reading about it online. Either way, I'm happy that I
# managed to come up with the equations despite not being very strong at this.
t1, t2, t3 = symbols("t1 t2 t3")
smx, smy, smz, vmx, vmy, vmz = symbols("smx smy smz vmx vmy vmz")

# Express the equations as a - b = 0 for the sympy solver.
eq1 = smx + vmx * t1 - positions[1][0] + velocities[1][0] * t1
eq2 = smy + vmy * t1 - positions[1][1] + velocities[1][1] * t1
eq3 = smz + vmz * t1 - positions[1][2] + velocities[1][2] * t1

eq4 = smx + vmx * t2 - positions[2][0] + velocities[2][0] * t2
eq5 = smy + vmy * t2 - positions[2][1] + velocities[2][1] * t2
eq6 = smz + vmz * t2 - positions[2][2] + velocities[2][2] * t2

eq7 = smx + vmx * t3 - positions[3][0] + velocities[3][0] * t3
eq8 = smy + vmy * t3 - positions[3][1] + velocities[3][1] * t3
eq9 = smz + vmz * t3 - positions[3][2] + velocities[3][2] * t3

# Returns the (smx, smy, smz, vmx, vmy, vmz, t1, t2, t3) params
solution = solve(
    [eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9],
    [smx, smy, smz, vmx, vmy, vmz, t1, t2, t3],
)[0]

# The part 2 puzzle solution is smx + smy + smz
print(solution[0] + solution[1] + solution[2])
