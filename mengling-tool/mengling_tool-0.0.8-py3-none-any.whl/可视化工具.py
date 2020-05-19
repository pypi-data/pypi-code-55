from matplotlib import pyplot as plt
import mengling_tool.mysql工具 as sqltools
import numpy as np

if __name__=='__main__':
    x = ['1', '2', '3']
    y = [12, 16, 6]
    sqltool_rmc = sqltools.mysqlExecutor('gprmc', host='rm-wz92k089rq29109m43o.mysql.rds.aliyuncs.com',
                                         user='mengling', passwd='Ljh246822')

    liedict, datas = sqltool_rmc.select(['时间区间', '盈利`+`亏损'], '策略4', where="`代码`='000032' and `过去天数`=1 and `涨跌幅域值`=5")
    arr_xy = np.array(datas)
    plt.bar(range(len(arr_xy[:, 0])), list(map(float,arr_xy[:, 1])), align='center')
    # plt.bar(x2, y2, color =  'g', align =  'center')
    plt.title('Bar graph')
    plt.ylabel('Y axis')
    plt.xlabel('X axis')
    plt.show()
