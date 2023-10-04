import os
import math

config_dir = os.path.join(os.path.expanduser('~'),'Repos/HeadedSocialForceModel/python_scripts/config/')

def bound_angle(angle):
    if (angle > math.pi): angle -= 2 * math.pi
    if (angle < -math.pi): angle += 2 * math.pi
    return angle

def main():
    radius = int(input("Specify the desired radius of the circular workspace (3, 4, 5, 6, or 7):\n"))
    n_actors = int(input("Specify the number of actors to insert in the experiment:\n"))

    ### COMPUTATIONS
    title = f"circular_op_hsfm_{n_actors}_{radius}m"
    arch = (2 * math.pi) / (n_actors)
    dist_center = radius - 0.5

    init_pos = []
    goal = []
    init_yaw = []

    for i in range(n_actors + 1):
        init_pos.append([round(dist_center * math.cos(arch * i),4), round(dist_center * math.sin(arch * i),4)])
        init_yaw.append(round(bound_angle(-math.pi + arch * i),4))
        goal.append([-init_pos[i][0],-init_pos[i][1]])

    ### GENERATE CONFIG FILE
    data = "# Starting positions\n"
    for i in range(n_actors):
        data += f"s[{i}] = [{init_pos[i][0]},{init_pos[i][1]}]\n"
    data += "\n# Waypoints\n"
    for i in range(n_actors):
        data += f"e_seq[{i}] = np.array([s[{i}],[{goal[i][0]},{goal[i][1]}],[{init_pos[i][0]},{init_pos[i][1]}]]).transpose()\n"
    data += "\n# Initial Yaw\n"
    for i in range(n_actors):
        data += f"th[{i}] = {init_yaw[i]}\n"

    with open(f'{config_dir}{title}.py', 'w') as file:
        file.write(data)

if __name__ == "__main__":
    main()