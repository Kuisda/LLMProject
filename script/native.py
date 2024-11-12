from tqdm import tqdm


import http.client
import sys
sys.path.append("..")
from utils import *
from interface import TextInterface,ResultInterface


if __name__ == "__main__":
    # load data
    questions,groundTruth = data_reader("mgsm_en","../data/mgsm_en/mgsm_en.jsonl")
    
    preds = []
    preds_ans = []
    
    # ask llm to get answer
    
    itf = TextInterface(
        model="gpt-4o-mini",
        task_name="mgsm_en",
        api_key="sk-LsPtaw73IsljGW9UxBXAxeQjOaIX6ErgULaa0jOltVy8YMRU",
        base_url="https://api.wlai.vip/v1",
        visitType="OpenAI_compa",
        extract_answer=answer_cleaning
    )
    
    # for question in tqdm(questions):
    #     pred = itf.call(prompt=question)
    #     pred_ans = itf.extract_answer(pred)
    #     preds.append(pred)
    #     preds_ans.append(pred_ans)



    #后续的部分要想正确的运行，必须保证数据集中的所有问题都保存在了一个jsonl文件中
    #如果llm请求出现中断，从断点重新开始请求会再开一个新的文件
    #我们最终需要把所有数据集中的所有数据都会汇总在一个jsonl文件夹中，然后用这个文件夹作为filePath
    filePath = getPredAndWrite(itf,questions,groundTruth,begin=0)

    preds,gt = readFromJsonl(filePath)
    
    preds_ans,gt = PostHandle(preds,gt)
    rtf = ResultInterface(
        len(questions),
        questions,preds,
        preds_ans,
        gt,
        method_name="Native",
        dataset='mgsm_en'
    )
    print(rtf.acc())
        
        
    