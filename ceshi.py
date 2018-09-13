def he():
    a = input("输入正数")
    b = input("输入负数")
    a = int(a)
    b = int(b)
    if b > 0:
        b *= -1
    max_len = 17  # 总长度
    sumx = []  # 容器
    if abs(a) > abs(b):  # 计算出正/负值需要的次数为负/正值的几倍
        beishu = abs(a//b)
        da = a
        xiao = b
    else:
        beishu = abs(b//a)
        da = b
        xiao = a

    # sep = 17//beishu  # 计算出一个数组中最多能出现多少个负数
    for i in range(max_len):
        if (i+1)%beishu == 0 and i != 0:
            sumx += [da]  # 添加绝对值大的
        else:
            sumx += [xiao]  # 添加绝对值小的
    print(sumx)
    print(sum(sumx))

he()
