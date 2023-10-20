import pandas as pd
import pickle

from constraints import URL_TRAM_MODELS


dfs = pd.read_html(URL_TRAM_MODELS)

# print(len(dfs))

# for table in range(len(dfs)):
#  print(dfs[table])

vbLine = dfs[0]
vbType = dfs[1]
vbTtss = dfs[2]

# print("vehicles by line :")
# print(vbLine)

# print(vbLine.info())

d = {
    '1': ['RF306', 'RF317', 'RF318', 'RF322', 'RF326', 'RF327', 'RF329', 'HK457', 'HK459'],
    '3': ['HY708', 'RY834', 'HY859', 'HY867', 'HY869', 'HY874', 'RY880'],
    '4': ['RG908', 'HG915', 'HG917', 'HG919', 'HG922', 'HG927', 'HG935'],
    '5': ['RF302', 'RF304', 'RF307', 'RF309', 'RF321'],
    '8': ['RY804', 'RY810', 'RY816', 'RY817', 'RY818', 'RY821', 'RY822', 'RY827'],
    '9': ['RP612', 'RP621', 'RP637', 'RP641', 'HY706', 'HY862', 'HY865'],
    '10': ['HY715', 'HY731', 'RY808', 'RY819', 'RY830', 'RY835', 'HY842', 'HY845', 'HY850', 'HY856'],
    '11': ['HL407', 'RP603', 'RP616', 'RP630', 'RP636', 'RP649'],
    '13': ['RP608', 'RP610', 'RP613', 'RP625', 'RP631', 'RP635', 'RP638', 'RP648'],
    '14': ['HY728', 'HY730', 'RY803', 'RY812', 'HY844', 'HY855', 'HY868'],
    '17': ['HL401', 'HL418', 'HL436', 'RP606', 'RP607', 'RP618', 'RP622'],
    '18': ['HY707', 'HY709', 'HY710', 'HY717', 'RY807', 'RY811', 'RY825', 'RY829', 'HY853', 'HY864', 'RY879', 'RY883'],
    '20': ['HL423', 'HL438', 'RP602', 'RP611', 'RP629', 'RP634', 'RP646'],
    '21': ['HW101', 'HW151', 'RW155', 'HL405', 'HK451'],
    '22': ['HY702', 'HY725', 'HY732', 'RY814', 'HY847', 'HY858'],
    '24': ['RY836', 'RY837', 'HY866', 'RY877', 'RY885', 'RG905', 'RG909'],
    '50': ['HY714', 'HY719', 'HY721', 'HY724', 'HY734', 'HY735', 'RY826', 'RY838', 'HY841', 'HY861', 'RY884', 'RG906',
           'RG907', 'RG913', 'RG914'],
    '52': ['RZ213', 'RZ226', 'RZ231', 'HZ255', 'HZ264', 'HZ278', 'HY718', 'HY860', 'HY863', 'HG923', 'HG926', 'HG928',
           'HG930', 'HG936'],
    '72': ['HL406', 'HL413', 'HL416', 'HL426', 'HL439', 'RP633']
}

with open('../generated/tramLines.pkl', 'wb') as fi:
    pickle.dump(d, fi)
