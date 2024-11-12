# 添加新的测试
1.在/data文件夹下创建对应的测试文件夹，具体数据使用jsonl格式进行存储
2.完善utils.data_reader；添加对应数据集名称到support_task 并 添加对应的读取实现
3.完善utils.answer_cleaning;support_task 并 添加对应的答案后置处理函数