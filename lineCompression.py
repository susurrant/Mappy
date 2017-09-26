import math

def compress(obj, s, e, threshod):    
    if e - s < 2:
        return
    
    maxDis = 0
    maxP = -1
    a = float(obj.y[e] - obj.y[s]) / (obj.x[e] - obj.x[s])
    b = float(obj.y[s]) - a * obj.x[s]
    deno = math.sqrt(a*a + 1)
    for i in range(s + 1, e):
        d = float(abs(a * obj.x[i] - obj.y[i] + b)) / deno
        if d > maxDis:
            maxP = i
            maxDis = d

    if maxDis > threshod:
        if maxP != -1:
            compress(obj, s, maxP, threshod)
            compress(obj, maxP, e, threshod)
    else:
        for i in range(1, e - s): #逆序删除
            del obj.x[e - i]
            del obj.y[e - i]
        
