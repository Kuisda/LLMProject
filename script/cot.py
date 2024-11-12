from tqdm import tqdm

import sys
sys.path.append("..")
from utils import *
from interface import TextInterface,ResultInterface


if __name__ == "__main__":
    # load data
    questions,groundTruth = data_reader("gsm8k","../data/gsm8k/test.jsonl")
    
    preds = []
    preds_ans = []
    
    # ask llm to get answer
    
    itf = TextInterface(
        model="GLM-4-Flash",
        task_name="gsm8k",
        api_key="api_key",
        base_url="base_url",
        visitType="OpenAI_compa",
        extract_answer=answer_cleaning
    )
    
    for question in tqdm(questions):
        prompt = ExampleBuild("./example/gsm8k",True)
        prompt = prompt + "Q:" + question + "\n"
        pred = itf.call(prompt=prompt)
        pred_ans = itf.extract_answer(pred)
        preds.append(pred)
        preds_ans.append(pred_ans)
    
    
    rtf = ResultInterface(
        len(questions),
        questions,preds,
        preds_ans,
        groundTruth,
        method_name="Native"
    )
    print(rtf.acc())
        
        
    