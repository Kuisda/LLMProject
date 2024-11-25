from typing import Callable, List,Optional,Any
from openai import OpenAI
import json
import re
from interface import ResultInterface,TextInterface
import datetime
from tqdm import tqdm

def data_reader(task:str,dataPath:str):
    '''
    read data with name task from dataPath  
    @return two list about Q,A:questions , answers
    '''
    support_task = ["gsm8k","mgsm_en"]
    questions = []
    answers   = []
    
    decoder = json.JSONDecoder()
    if task not in support_task:
        raise ValueError("unsupport task:",task)
    if task == "gsm8k":
        with open(dataPath) as f:
            lines = f.readlines()
            for line in lines:
                json_res = decoder.raw_decode(line)[0]
                questions.append(json_res["question"].strip())
                answers.append(json_res["answer"].split('#### ')[-1])
    elif task == "mgsm_en":
        for line in open(dataPath):
            questions.append(json.loads(line)['input']) 
            answers.append(json.loads(line)['target'])
    print("dataset:{}".format(task))
    print("data size:{}".format(len(answers)))
    
    return questions,answers

def handle_zero(s:str)->str:
    '''
    2.000->2
    2.00->2
    '''
    if s.find('.') == -1:
        return s
    sList = s.split('.')
    assert len(sList) == 2
    after_part = sList[-1]
    for ch in after_part:
        if ch !='0':
            return s
    return sList[0]


def answer_cleaning(task:str,pred:str):
    '''
    pred will be a problem's response from llm ,it may contain mulitiple numbers
    
    '''
    # print("before clean:" + pred)
    
    support_task = ["gsm8k","mgsm_en"]
    if task not in support_task:
        raise ValueError("unsupport task:",task)
    
    if task == "gsm8k" or "mgsm_en":
        pred = pred.replace(",", "")
        pred = [s for s in re.findall(r'-?\d+\.?\d*', pred)]

        if len(pred) == 0 :
            pred = ""
        else:
            pred = pred[-1]
        
        # handle if word ends with '.'
        if pred !="" and pred[-1] == ".":
            pred = pred[:-1]
        
        
        # print("after clean:" + pred)

        return handle_zero(pred)
    

def compare_Methods(rtf1:ResultInterface,rtf2:ResultInterface,saveDir:str = "./",fileName:str=None):
    '''
    comapre result between two methods
    1.the accuracy
    2.both False or only False
    '''
    assert rtf1.dataset == rtf2.dataset
    if fileName is None:
        fileName = rtf1.method_name + "__" + rtf2.method_name
    filePath = saveDir + fileName
    only1List = []
    only2List = []
    bothList  = []
    with open(filePath,mode='a',encoding="utf-8") as f:
        f.writelines("Total:",rtf1.total)
        f.writelines(rtf1.method_name+":" + rtf1.correctNum)
        f.writelines(rtf2.method_name+":" + rtf2.correctNum)
        for i in range(rtf1.total):
            if i in rtf1.FalseList and i not in rtf2.FalseList:
                only1List.append(i)
            elif i not in rtf1.FalseList and i in rtf2.FalseList:
                only2List.append(i)
            elif i in rtf1.FalseList and i in rtf2.FalseList:
                bothList.append(i)
        f.writelines("count for both false:" + len(bothList))
        f.writelines("count for only " + rtf1.method_name + " false:" + len(only1List))
        f.writelines("count for only " + rtf2.method_name + " false:" + len(only2List))
        f.write('='*60 + '\n\n\n')
        
        f.write("<<" + rtf1.method_name + "False>>\n")
        f.write("The " + rtf1.method_name + "pred is false while " + rtf2.method_name + "pred is true")
        f.write("\n\n\n")
        
        for i in only1List:
            f.write("[Questions]:\n")
            f.write(rtf1.questions[i] + "\n")
            f.write("\n\n\n")
            f.write("[" + rtf1.method_name + "pred]:\n")
            f.write(rtf1.preds[i])
            f.write("\n\n\n")
            f.write("extract_answer:" + rtf1.preds_ans[i])
            f.write("[" + rtf2.method_name + "pred]:\n")
            f.write(rtf2.preds[i])
            f.write("\n\n\n")
            f.write("extract_answer:" + rtf2.preds_ans[i])
            f.write("\n\n\n")
            f.write("groundTruth:" + rtf1.groundTruth[i])
            f.write("\n\n\n")
        
        f.write('='*60 + '\n')
        f.write("<<" + rtf2.method_name + "False>>\n")
        f.write("The " + rtf1.method_name + "pred is true while " + rtf2.method_name + "pred is false")
        for i in only2List:
            f.write("[Questions]:\n")
            f.write(rtf1.questions[i] + "\n")
            f.write("\n\n\n")
            f.write("[" + rtf1.method_name + "pred]:\n")
            f.write(rtf1.preds[i])
            f.write("\n\n\n")
            f.write("extract_answer:" + rtf1.preds_ans[i])
            f.write("[" + rtf2.method_name + "pred]:\n")
            f.write(rtf2.preds[i])
            f.write("\n\n\n")
            f.write("extract_answer:" + rtf2.preds_ans[i])
            f.write("\n\n\n")
            f.write("groundTruth:" + rtf1.groundTruth[i])
            f.write("\n\n\n")
        
        f.write('='*60 + '\n')
        f.write("<<Both False>>\n")
        f.write("The " + rtf1.method_name + "pred is false while " + rtf2.method_name + "pred is false")
        for i in bothList:
            f.write("[Questions]:\n")
            f.write(rtf1.questions[i] + "\n")
            f.write("\n\n\n")
            f.write("[" + rtf1.method_name + "pred]:\n")
            f.write(rtf1.preds[i])
            f.write("\n\n\n")
            f.write("extract_answer:" + rtf1.preds_ans[i])
            f.write("[" + rtf2.method_name + "pred]:\n")
            f.write(rtf2.preds[i])
            f.write("\n\n\n")
            f.write("extract_answer:" + rtf2.preds_ans[i])
            f.write("\n\n\n")
            f.write("groundTruth:" + rtf1.groundTruth[i])
            f.write("\n\n\n")
            
def getPredAndWrite(
        itf:TextInterface,
        questions:List[str],
        groundTruth:List[str],
        format_instruction = "\nYour final answer should be a single numerical number, put the number at the end of your whole response with format like:'Answer: [final answer]'",
        begin:int=0)->str:
    '''
    对每一道题目发送请求，获取结果，并写入文件夹
    这么做的原因是因为请求可能中断或者出问题，此时方便按照题号进行接下来的题目处理，而不用重新跑
    如果出现了请求断流，需要把属于同一个问题集的数据汇总在同一个jsonl文件中，并以这个文件作为filepath
    '''
    now = datetime.datetime.now()
    timestamp_str = now.strftime('%Y-%m-%d-%H-%M-%S')
    filePath = f'../result/{itf.task_name}_{itf.model}_{timestamp_str}.jsonl'

    length = len(questions)
    with open(filePath,mode='a') as f:
        for i in tqdm(range(length)):
            if begin !=0:
                begin -=1
                continue
            question = questions[i]
            gt = groundTruth[i]
            prompt = question + format_instruction
            pred = itf.call(prompt=prompt)
            # pred_ans = itf.extract_answer(pred)
            # gt_clean = itf.extract_answer(gt)
            # tmp = {'Question':question,'Pred':pred,'Pred_ans':pred_ans,'GT':gt,'GT_clean':gt_clean}
            #这个函数应该仅仅储存llm的回复结果，后置处理应该与llm的回答解耦
            tmp = {'Question':question,'Pred':pred,'GT':gt}
            json_str = json.dumps(tmp)
            f.write(json_str + '\n')
    print('save as:' + filePath)
    return filePath

def readFromJsonl(filePath:str):
    '''
    from result jsonl file get two list : preds,gt
    '''
    preds = []
    gt = []

    for line in open(filePath):
        preds.append(json.loads(line)['Pred'])
        gt.append(json.loads(line)['GT'])
    
    return preds,gt

def PostHandle(task:str,preds:List[str],gt:List[str]):
    '''
    use answer_cleaning as rule in task to two list : preds and gt and then return
    '''
    preds = [answer_cleaning(task,s) for s in preds]
    gt    = [answer_cleaning(task,s) for s in gt]

    return preds,gt

            
def ExampleBuild(examplePath:str ,cot_flag:str)->str:
    '''
    load few shot example from examplePath
    each example will like:(question + (cot)? + answer) 
    
    example in file should be structed as json format
    '''
    x,y,z = [],[],[]
    with open(examplePath, encoding="utf-8") as f:
        json_data = json.load(f)
        json_data = json_data["example"]
        for line in json_data:
            x.append(line["question"])
            y.append(line["rationale"])
            z.append(line["pred_ans"])
        
    text = ""
    for i in range(len(x)):
        if cot_flag:
            text +=x[i] + " " + y[i] + " " + "The answer is:" + z[i] + ".\n\n"
        else:
            text +=x[i] + " " + "The answer is" + z[i] + ".\n\n"
    return text
    