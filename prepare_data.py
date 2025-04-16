# 该代码用于从rqsdk库中下载线数据，下载的数据保存在data中

import rqdatac
import datetime
import pandas

# ricequant信息的初始化，保证后续能调用api接口
rqdatac.init('18720946768','20060402lyf')

