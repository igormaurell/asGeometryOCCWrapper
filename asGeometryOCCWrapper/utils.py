
def list2tcol1d(l, tcol_tp, data_tp):
    length = len(l)
    tcol = tcol_tp(1, length)
    for i in range(length):
        d = l[i]
        if hasattr(d, '__iter__'):
            tcol.SetValue(i + 1, data_tp(*d))
        else:
            tcol.SetValue(i + 1, data_tp(d))
    return tcol

def list2tcol2d(l, tcol_tp, data_tp):
    print(l)
    length1 = len(l)
    length2 = len(l[0])
    tcol = tcol_tp(1, length1, 1, length2)
    for i in range(length1):
        for j in range(length2):
            d = l[i][j]
            if hasattr(d, '__iter__'):
                tcol.SetValue(i + 1, j + 1, data_tp(*d))
            else:
                tcol.SetValue(i + 1, j + 1, data_tp(d))
    return tcol