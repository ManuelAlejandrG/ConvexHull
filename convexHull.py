import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cw_next = None
        self.ccw_next = None

    def subtract(self, p):
        return Point(self.x - p.x, self.y - p.y)

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y
    
def direction(a,b,c):
    res = (b.y - a.y) * (c.x - b.x) - (c.y - b.y)* (b.x - a.x)
    if res >= 0:
        return 1
    else:
        return -1
    
def merge(hull1, hull2):
    p = max(hull1, key = lambda point: point.x)

    q = min(hull2, key = lambda point: point.x)
    cp_p = p
    cp_q = q

    prev_p = None
    prev_q = None
    while (True):
        prev_p = p
        prev_q = q
        if q.cw_next:
            # mover p en sentido horario siempre que gire a izquierda 
            while direction(p, q, q.cw_next) < 0:
                q = q.cw_next
        if p.ccw_next:
            # mover p siempre que gire a la derecha
            while direction(q, p, p.ccw_next) > 0:
                p = p.ccw_next

        if p == prev_p and q == prev_q:
            break
    
    prev_p = None
    prev_q = None
    while (True):
        prev_p = cp_p
        prev_q = cp_q
        if cp_q.ccw_next:
            # mover p siempre que gire a derecha 
            while direction(cp_p, cp_q, cp_q.ccw_next) > 0:
                cp_q = cp_q.ccw_next
        if cp_p.cw_next:
            # # mover p siempre que gire a la izquierda
            while direction(cp_q, cp_p, cp_p.cw_next) < 0:
                cp_p = cp_p.cw_next
        if cp_p == prev_p and cp_q == prev_q:
            break

    # borrar
    p.cw_next = q
    q.ccw_next = p

    cp_p.ccw_next = cp_q
    cp_q.cw_next = cp_p

    # resultado
    result = []
    start = p 
    while (True):
        result.append(p)
        p = p.ccw_next

        if p == start:
            break
            
    return result



def convex_hull(points):
    if len(points) == 1:
        return points

    left_half = convex_hull(points[0: int(len(points)/2)])
    right_half = convex_hull(points[int(len(points)/2):])
    return merge(left_half, right_half)

if __name__ == '__main__':
    
    
    p1 = Point(0, 0)
    p2 = Point(1, -4)
    p3 = Point(-1, -5)
    p4 = Point(-5,-3)
    p5 = Point(-3, -1)
    p6 = Point(-1, -3)
    p7 = Point(-2,-2)
    p8 = Point(-2, -1)
    
    points =[p1,p2,p3,p4,p5,p6, p7, p8]
    points = sorted(points, key = lambda p: p.x)
    c = convex_hull(points)
    
    x, y = [], []
    for i in points:
        x.append(i.x)
        y.append(i.y)
    
    xc, yc = [], []
    for i in c:
        xc.append(i.x)
        yc.append(i.y)
        
    plt.figure()    
    plt.scatter(x,y, label="inner")
    plt.scatter(xc,yc, label="convex hull")
    plt.legend()
    plt.show()
        