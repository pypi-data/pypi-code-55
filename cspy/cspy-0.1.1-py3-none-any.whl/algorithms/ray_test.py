import ray


class search:

    def __init__(self, direction, pos):
        self.direction = direction
        self.pos = pos

    def move(self, pos_max):
        while True:
            if self.direction == "forward" and self.pos < pos_max:
                print("forward", self.pos)
                self.pos += 1
            elif self.pos > pos_max:
                print("backward", self.pos)
                self.pos -= 1
            else:
                break

    def get_pos(self):
        return self.pos


def start_parallel(n=10000):
    Actor = ray.remote(num_cpus=2)(search)
    workers = [
        Actor.remote(d, pos) for d, pos in [("forward", 0), ("backward", n)]
    ]
    s = search.remote("forward", 0)
    f_pos = 0
    sb = search.remote("backward", n)
    b_pos = n
    for i in range(n):
        s.move.remote(b_pos)
        sb.move.remote(f_pos)
        f_pos = ray.get(s.get_pos.remote())
        b_pos = ray.get(sb.get_pos.remote())


def start(n=10000):
    s = search("forward", 0)
    for i in range(n):
        s.move(n)


ray.init(num_cpus=2)
# No interactions
#s = search.remote("forward", 0)
#sb = search.remote("backward", 10)
#for i in range(10):
#    s.move.remote()
#    sb.move.remote()
#result = ray.get(s.get_pos.remote())
#print(result)
#result = ray.get(sb.get_pos.remote())
#print(result)

start_parallel()
