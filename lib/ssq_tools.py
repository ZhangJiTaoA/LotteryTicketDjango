import array
from lib.data_tools import SSQ_data

from lib.lt_tools import lt_tools
from etc import constant


class SSQ:

    def __init__(self):
        self.tools = lt_tools()
        self.data = SSQ_data()

    # 生成一个双色球序列
    def create_ssq(self):
        redArr = self.tools.create_randoms_num(constant.ssq_red_start, constant.ssq_red_end, constant.ssq_red_length)
        blueArr = self.tools.create_randoms_num(constant.ssq_blue_start, constant.ssq_blue_end,
                                                constant.ssq_blue_length)

        redArr.extend(blueArr)
        print("生成双色球数组：", redArr)
        return redArr

    # 查询与给入seq最相似的n条数据的期数,返回查到的具体数据及查到的数量n
    # 输入为[red1,red2,red3,red4,red5,red6,blue]
    def query_similar_ssq(self, seq):
        data = self.data.get_dataframe()
        n = 6
        while (n > 0):
            redResult = self.tools.get_similar_seq(
                df=data.loc[:, ['issue', 'red1', 'red2', 'red3', 'red4', 'red5', 'red6']],
                seq=seq[0:6],
                n=n)
            if (redResult.empty == False):
                break
            n = n - 1

        blueResult = self.tools.get_similar_seq(df=data.loc[:, ['issue', 'blue']], seq=seq[6:7], n=1)
        result = blueResult[blueResult.isin(redResult)]  # 篮球相同并且红球有n个相同的期数
        if (result.empty == True):
            return data[data['issue'].isin(redResult)], n
        else:
            return data[data['issue'].isin(result)], n + 1


if __name__ == '__main__':
    ssq = SSQ()
    a_ssq = ssq.create_ssq()
    data, n = ssq.query_similar_ssq(a_ssq)

    print(f"历史上最多共有{n}球个相同，共{len(data)}条数据，具体数据为{data}")
