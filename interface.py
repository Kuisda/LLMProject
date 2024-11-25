from typing import Callable, List,Optional,Any
from openai import OpenAI
import json
import re


class TextInterface:
    def __init__(
        self,
        model:str = 'code-davinci-002',
        task_name:str=None,
        api_key:str = None,
        base_url:str = None,
        visitType:str = "OpenAI",#["OpenAI","OpenAI_compa"]
        stop: str = None,
        #Callable[[str,str], Any]表示接收两个参数，返回值为任意
        extract_answer: Optional[Callable[[str,str], Any]] = None,
        ) -> None:
        supportTypes = ["OpenAI","OpenAI_compa"]
        if visitType not in supportTypes:
            raise ValueError("visitType doesn't support,please choose:" + supportTypes)
        if visitType == "OpenAI":
            client = OpenAI(
                api_key=api_key
            )
            self.client = client
        else: #visitType == "OpenAI_compa"
            client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
            self.client = client
        
        self.history = [{"role": "system", "content": "You are an excellent math problem solver "}]
        self.extract_answer_fn = extract_answer
        self.stop = stop
        self.model = model
        self.task_name = task_name
    
    def clear_history(self):
        self.history = []
        
    def extract_answer(self, gen: str):
        if self.extract_answer_fn:
            return self.extract_answer_fn (self.task_name,gen)
        gen = [s for s in re.findall(r'-?\d+\.?\d*', gen)]
        if len(gen) == 0:
            gen = ""
        else:
            gen = gen[-1]
            if gen[-1] == ".":
                gen = gen[:-1]
        return gen

    def call(self, prompt, temperature=0.0, top_p=1.0, majority_at=None, max_tokens=512,meta_prompt:str = None,History_Input:bool = False):
        '''
        History_Input: if true,each round's input will contain historical dialogue
        '''
        self.history += [{"role":"user","content":prompt}]
        if History_Input == False:
            if meta_prompt is None:
                meta_prompt = "You are an excellent math problem solver "
            completion = self.client.chat.completions.create(
                model = self.model,
                messages=[
                    {"role": "system", "content": meta_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stop=self.stop,
            )
            # print(completion)
            gen = completion.choices[0].message.content
        else:
            self.history += [{"role":"user","content":prompt}]
            completion = self.client.chat.completions.create(
                model = self.model,
                messages=self.history,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stop=self.stop,
            )
            gen = completion.choices[0].message.content
            
        self.history += [{"role":"assistant","content":gen}]
        return gen
    
    def restrict_call(self, meta_prompt:str,prompt:str, restriction:List[str],retry:int = 16)->str:
        '''
        设置合法输出，并且使用多次请求保证一定会得到一个合法输出
    for example:
    {{#system}}YOU ARE one of the GREATEST mathematicians, logicians, programmers, and AI scientists. You are intelligent and rational. You are prudent and cautious. Your mastery over Arithmetic, Combinatorics, Number Theory, Probability Theory, Algebra, Analysis, and Geometry is unparalleled. You THINK NATURAL, BROAD AND DEEP. Let's think step by step. {{/system}}
    {{#system}}Your job is to judge whether the "answer" and "last_answer" are equivalent. Do not be strict on the format, but check the content. {{/system}}
    {{#user}}
    Problem Subject: "{{question_subject}}", 
    Problem Content: "{{question_content}}"
    Are the "answer" and "last_answer" are equivalent? Reply with Equivalent or Different.
    "answer": "{{answer}}"
    "last_answer": "{{last_answer}}"
    {{/user}}
    {{#assistant}}{{select "equivalence" options=valid_equivalence}}{{/assistant}}
        '''
        if len(restriction) == 0:
            raise ValueError("the restriction is empty,which means none of the answer is valid")
        try_cnt = 0
        while try_cnt < retry:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "YOU ARE one of the GREATEST mathematicians, logicians, programmers, and AI scientists. You are intelligent and rational. You are prudent and cautious. Your mastery over Arithmetic, Combinatorics, Number Theory, Probability Theory, Algebra, Analysis, and Geometry is unparalleled. You THINK NATURAL, BROAD AND DEEP. Let's think step by step. "},
                    {"role":"system","content":meta_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            gen = completion.choices[0].message.content
            for valid_answer in restriction:
                if valid_answer in gen:
                    return valid_answer
                
        
    
class ResultInterface:
    def __init__(
        self,
        total:int,
        questions:List[str],
        preds:List[str],
        preds_ans:List[str],
        groundTruth:List[str],
        method_name:str,
        dataset:str,
    ):
        '''
        questions: the list of questions
        groundTruth: the list of groundTruth for each question
        preds:the list of llm response for each question
        preds_ans: the list of extract answer from llm response for each question
        '''
        assert len(questions) == len(preds) == len(groundTruth) == len(preds_ans) == total
        self.questions = questions
        self.total = total
        self.preds = preds
        self.preds_ans = preds_ans
        self.groundTruth = groundTruth
        self.method_name = method_name
        self.dataset = dataset
        self.FalseList = []
        correct = 0
        for i in range(total):
            if preds_ans[i] == groundTruth[i]:
                correct +=1
            else:
                self.FalseList.append(i)
        self.correctNum = correct
    def acc(self):
        return self.correctNum / self.total

    def saveToDir(self,saveDir:str):
        '''
        save result to saveDir,for each question ,contain llm pred,ans extract from pred and groundTruth
        '''
        with open(saveDir,mode = 'a') as f:
            for i in range(len(self.questions)):
                tmp = {"Question":self.questions[i],"Pred":self.preds[i],"Pred_ans":self.preds_ans[i],"GT":self.groundTruth[i]}
                json_str = json.dumps(tmp)
                f.write(json_str + '\n')
                # f.write("[Questions]:\n")
                # f.write(self.questions[i] + "\n")
                # f.write("\n\n\n")
                # f.write("[pred]:\n")
                # f.write(self.preds[i] + "\n")
                # f.write("\n\n\n")
                # f.write("[pred_ans]:\n")
                # f.write(self.preds_ans[i] + "\n")
                # f.write("[groundTruth]:")
                # f.write(self.groundTruth[i] + "\n")
                # f.write("-"*60)
    def saveFault(self,filepath:str = './FaultResult.jsonl'):
        '''
        print and save to file about Fault problem
        '''
        with open(filepath,mode='a') as f:
            for i in self.FalseList:
                tmp = {'Problem':self.questions[i],'Pred':self.preds[i],'Pred_ans':self.preds_ans[i],'GT':self.groundTruth[i]}
                json_str = json.dumps(tmp)
                f.write(json_str + '\n')
            

        
        
                
    