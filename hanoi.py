import sys
from itertools import permutations, product, combinations


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    domain_file.write("Proposition:\n")
    # Clear
    for disk, peg in product(disks, pegs):
        clear_com = f"clear_{disk}_{peg} "
        domain_file.write(clear_com)
    
    # OnTop
    for disk1, disk2 in combinations(disks, 2):
        on_top_com = f"on_top_{disk1}_{disk2} "
        domain_file.write(on_top_com)

    # Empty
    for peg in pegs:
        empty_com = f"empty_{peg} "
        domain_file.write(empty_com)

    # Ground
    for disk, peg in product(disks, pegs):
        ground_com = f"ground_{disk}_{peg} "
        domain_file.write(ground_com)

    domain_file.write("\nActions:\n")

    # 3 Disks action
    total_disks = [(disk1, disk2, disk3) for i, disk1 in enumerate(disks) for disk2, disk3 in permutations(disks[i + 1:],2)]
    for disks_l, pegs_l in product(total_disks, combinations(pegs,2)):
        peg1, peg2 = pegs_l
        disk1, disk2, disk3 = disks_l
        action_name = f"Name: move3_{disk1}_{disk2}_{disk3}_{peg1}_{peg2}\n" 
        pre_and_delete = f"on_top_{disk1}_{disk2} clear_{disk1}_{peg1} clear_{disk3}_{peg2}\n"
        pre = f"pre: {pre_and_delete}"
        add = f"add: clear_{disk2}_{peg1} clear_{disk1}_{peg2} on_top_{disk1}_{disk3}\n"
        delete = f"delete: {pre_and_delete}"
        domain_file.writelines([action_name, pre, add, delete])

    # 2 Disks action to empty
    for disk1, disk2 in combinations(disks,2):
        for peg1, peg2 in combinations(pegs,2):
            action_name = f"Name: move_to_empty_{disk1}_{disk2}_{peg1}_{peg2}\n"
            pre_and_delete = f"empty_{peg2} on_top_{disk1}_{disk2} clear_{disk1}_{peg1}\n"
            pre = f"pre: {pre_and_delete}"
            add = f"add: clear_{disk1}_{peg2} ground_{disk1}_{peg2} clear_{disk2}_{peg1}\n"
            delete = f"delete: {pre_and_delete}"
            domain_file.writelines([action_name, pre, add, delete])

    # 2 Disks action from ground
    for disk1, disk2 in combinations(disks,2):
        for peg1, peg2 in combinations(pegs,2):
            action_name = f"Name: move_from_ground_{disk1}_{disk2}_{peg1}_{peg2}\n"
            pre_and_delete = f"ground_{disk1}_{peg1} clear_{disk2}_{peg2} clear_{disk1}_{peg1}\n"
            pre = f"pre: {pre_and_delete}"
            add = f"add: on_top_{disk1}_{disk2} empty_{peg1} clear_{disk1}_{peg2}\n"
            delete = f"delete: {pre_and_delete}"
            domain_file.writelines([action_name, pre, add, delete])

    # Ground to Empty Action
    for disk1 in disks:
        for peg1, peg2 in combinations(pegs,2):
            action_name = f"Name: move_from_ground_to_empty_{disk1}_{peg1}_{peg2}\n"
            pre_and_delete = f"ground_{disk1}_{peg1} clear_{disk1}_{peg1} empty_{peg2}\n"
            pre = f"pre: {pre_and_delete}"
            add = f"add: empty_{peg1} clear_{disk1}_{peg2} ground_{disk1}_{peg2}\n"
            delete = f"delete: {pre_and_delete}"
            domain_file.writelines([action_name, pre, add, delete])
    domain_file.close()


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file
    # Empty pegs
    problem_file.write("Initial state: ")
    for peg in pegs[1:]:
        problem_file.write(f"empty_{peg} ")
    
    # Stack disks
    for i, disk in enumerate(disks[:-1]):
        problem_file.write(f"on_top_{disk}_{disks[i+1]} ")
    
    problem_file.write(f"ground_{disks[-1]}_{pegs[0]} ")
    problem_file.write(f"clear_{disks[0]}_{pegs[0]}")

    # Empty pegs
    problem_file.write("\nGoal state: ")
    for peg in pegs[:-1]:
        problem_file.write(f"empty_{peg} ")
    
    # Stack disks
    for i, disk in enumerate(disks[:-1]):
        problem_file.write(f"on_top_{disk}_{disks[i+1]} ")
    
    problem_file.write(f"ground_{disks[-1]}_{pegs[-1]} ")
    problem_file.write(f"clear_{disks[0]}_{pegs[-1]}")

    problem_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
