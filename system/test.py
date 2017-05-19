from evidence_retrieval.data_source import DataSource
from evidence_retrieval.data_source import ChineseTokenizer
import os
a = DataSource
print(a.get_evidence('牙疼'))

# ..
print(os.pardir)
# 当前文件夹路径
print(os.path.dirname(__file__))
# 上层路径
print(os.path.abspath(os.path.dirname(__file__)+os.path.sep+os.pardir))
# /
print(os.path.sep)

print(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
# 上上层路径
print(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)))
