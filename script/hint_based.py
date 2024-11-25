from tqdm import tqdm

import sys
sys.path.append("..")
from utils import *
from interface import TextInterface,ResultInterface

hint_template = '''
Q:Jenna is hemming her prom dress. The dress's hem is 3 feet long. Each stitch Jenna makes is 1/4 inch long. If Jenna makes 24 stitches per minute, how many minutes does it take Jenna to hem her dress?

Hint 1: Convert units
The dress hem length is given in feet, and each stitch is given in inches. To calculate how many stitches are needed to hem the entire dress, it's helpful to convert the dress length from feet to inches.

Hint 2: Calculate the total number of stitches required
Once we know the dress length in inches, we can determine how many stitches Jenna will need by dividing the total length by the length of each stitch.

Hint 3: Use the rate of stitches per minute
Now that we know the total number of stitches required, we can calculate the time it takes by using Jenna’s stitching rate (24 stitches per minute).

Hint 4: Solve for time
Divide the total number of stitches by Jenna's stitching rate to find the total time needed in minutes.


Q:A company has 1000 employees. There will be three rounds of layoffs. For each round of layoff, 10% of the remaining employees will be laid off. How many employees will be laid off in total?

To approach this question effectively, let’s break it down with a series of intermediate hints:

Hint 1: Understand the Percentage Layoff per Round
Each round will lay off 10% of the remaining employees, not the original total. Therefore, we need to adjust the employee count after each round before calculating the next layoff amount.

Hint 2: Calculate Employees Laid Off in Each Round
For each round, calculate 10% of the current number of employees. Subtract this from the remaining total after each round to update the employee count.

Hint 3: Keep Track of Total Layoffs
Sum up the employees laid off in each of the three rounds to get the final total.

Hint 4: Solve for the Total Layoff
After calculating the layoffs for each round and adding them together, we’ll arrive at the final answer for the total number of employees laid off.

Q:A busy port has 4 cruise ships and twice as many cargo ships. The number of sailboats is 6 more than the cargo ships and seven times more than fishing boats. How many vessels are there on the water?

Hint 1: Define the Variables
Identify the different types of vessels: cruise ships, cargo ships, sailboats, and fishing boats. Assign variables where needed for unknown values.

Hint 2: Relate Cargo Ships to Cruise Ships
The problem states that the number of cargo ships is twice the number of cruise ships. Since we know the number of cruise ships, calculate the number of cargo ships.

Hint 3: Calculate the Number of Sailboats
The number of sailboats is defined in relation to the cargo ships. Use the value of cargo ships to find the number of sailboats.

Hint 4: Relate Fishing Boats to Sailboats
According to the problem, the number of sailboats is seven times the number of fishing boats. Use this information to solve for the number of fishing boats.

Hint 5: Sum All Vessel Counts
Once each vessel type has been quantified, add them up to determine the total number of vessels on the water.

Q:John adopts a dog from a shelter.  The dog ends up having health problems and this requires 3 vet appointments,  which cost $400 each.  After the first appointment, John paid $100 for pet insurance that covers 80% of the subsequent visits.  How much did he pay in total?

To approach this question, here are some intermediate hints:

Hint 1: Identify the Costs of Each Vet Appointment
Determine the cost of each of the three vet appointments and identify which appointments are covered by insurance.

Hint 2: Calculate the Cost of the First Appointment
Since the insurance was purchased after the first appointment, John pays the full cost for this appointment.

Hint 3: Apply Insurance Coverage for the Subsequent Appointments
For the second and third appointments, calculate the amount John pays out-of-pocket after insurance covers 80% of the costs.

Hint 4: Sum Up All Expenses
Include the cost of the first appointment, the insurance payment, and the out-of-pocket expenses for the covered appointments to find the total amount John paid.

Q:{Question}
'''

answer_template ='''
Q:Jenna is hemming her prom dress. The dress's hem is 3 feet long. Each stitch Jenna makes is 1/4 inch long. If Jenna makes 24 stitches per minute, how many minutes does it take Jenna to hem her dress?

Hint 1: Convert units
The dress hem length is given in feet, and each stitch is given in inches. To calculate how many stitches are needed to hem the entire dress, it's helpful to convert the dress length from feet to inches.

Hint 2: Calculate the total number of stitches required
Once we know the dress length in inches, we can determine how many stitches Jenna will need by dividing the total length by the length of each stitch.

Hint 3: Use the rate of stitches per minute
Now that we know the total number of stitches required, we can calculate the time it takes by using Jenna’s stitching rate (24 stitches per minute).

Hint 4: Solve for time
Divide the total number of stitches by Jenna's stitching rate to find the total time needed in minutes.

A:To solve this, let’s follow each hint step by step:
1.Convert units:
The dress hem is 3 feet long, and we need to convert this to inches because each stitch is given in inches.
3 feet×12 inches per foot=36 inches
2.Calculate the total number of stitches required:
Each stitch is 1/4inch long. So, the total number of stitches needed is:
36 inches/ (1/4) inch per stitch = 36 x 4 = 144 stitches
3.Use the rate of stitches per minute:
Jenna makes 24 stitches per minute.
4.Solve for time:
Divide the total number of stitches by Jenna's stitching rate to find the total time in minutes.
144 stitches / 24 stitches per minute = 6 minutes

The Answer is 6 minutes.


Q:A company has 1000 employees. There will be three rounds of layoffs. For each round of layoff, 10% of the remaining employees will be laid off. How many employees will be laid off in total?

Hint 1: Understand the Percentage Layoff per Round
Each round will lay off 10% of the remaining employees, not the original total. Therefore, we need to adjust the employee count after each round before calculating the next layoff amount.

Hint 2: Calculate Employees Laid Off in Each Round
For each round, calculate 10% of the current number of employees. Subtract this from the remaining total after each round to update the employee count.

Hint 3: Keep Track of Total Layoffs
Sum up the employees laid off in each of the three rounds to get the final total.

Hint 4: Solve for the Total Layoff
After calculating the layoffs for each round and adding them together, we’ll arrive at the final answer for the total number of employees laid off.

A:Following the hints step-by-step:

1.First Round of Layoffs:
Initial number of employees = 1000
Lay off 10% of 1000:1000×0.10=100 employees
Remaining employees after the first round:1000−100=900
2.Second Round of Layoffs:
Starting with 900 employees, lay off 10%:900×0.10=90 employees
Remaining employees after the second round:900−90=810
3.Third Round of Layoffs:
Starting with 810 employees, lay off 10%:810×0.10=81 employees
Remaining employees after the third round:810−81=729
4.Total Layoffs:
Add up the employees laid off in each round:100+90+81=271

The Answer is 271.


Q:A busy port has 4 cruise ships and twice as many cargo ships. The number of sailboats is 6 more than the cargo ships and seven times more than fishing boats. How many vessels are there on the water?

Hint 1: Define the Variables
Identify the different types of vessels: cruise ships, cargo ships, sailboats, and fishing boats. Assign variables where needed for unknown values.

Hint 2: Relate Cargo Ships to Cruise Ships
The problem states that the number of cargo ships is twice the number of cruise ships. Since we know the number of cruise ships, calculate the number of cargo ships.

Hint 3: Calculate the Number of Sailboats
The number of sailboats is defined in relation to the cargo ships. Use the value of cargo ships to find the number of sailboats.

Hint 4: Relate Fishing Boats to Sailboats
According to the problem, the number of sailboats is seven times the number of fishing boats. Use this information to solve for the number of fishing boats.

Hint 5: Sum All Vessel Counts
Once each vessel type has been quantified, add them up to determine the total number of vessels on the water.

A:Following each hint step-by-step:
1.Define the Variables:
Cruise ships = 4
Let the number of cargo ships be C.
Let the number of sailboats be S.
Let the number of fishing boats be F.

2.Relate Cargo Ships to Cruise Ships: The number of cargo ships is twice the number of cruise ships
C=2×4=8

3.Calculate the Number of Sailboats: The number of sailboats is 6 more than the number of cargo ships.
S=C+6=8+6=14

4.Relate Fishing Boats to Sailboats: The number of sailboats is seven times the number of fishing boats.
S=7×F
Solving for F:
F = S/7 = 14/7 = 2

5.Sum All Vessel Counts: Total number of vessels = cruise ships + cargo ships + sailboats + fishing boats.
4+8+14+2=28

The Answer is 28.


Q:John adopts a dog from a shelter.  The dog ends up having health problems and this requires 3 vet appointments,  which cost $400 each.  After the first appointment, John paid $100 for pet insurance that covers 80% of the subsequent visits.  How much did he pay in total?

Hint 1: Identify the Costs of Each Vet Appointment
Determine the cost of each of the three vet appointments and identify which appointments are covered by insurance.

Hint 2: Calculate the Cost of the First Appointment
Since the insurance was purchased after the first appointment, John pays the full cost for this appointment.

Hint 3: Apply Insurance Coverage for the Subsequent Appointments
For the second and third appointments, calculate the amount John pays out-of-pocket after insurance covers 80% of the costs.

Hint 4: Sum Up All Expenses
Include the cost of the first appointment, the insurance payment, and the out-of-pocket expenses for the covered appointments to find the total amount John paid.

A:Following each hint step-by-step:
1.Identify the Costs of Each Vet Appointment:
Each appointment costs $400. There are three appointments in total.
2.Calculate the Cost of the First Appointment:
Since insurance was purchased after the first appointment, John pays the full $400 for this appointment.
3.Apply Insurance Coverage for the Subsequent Appointments:
After the first appointment, John purchases insurance for $100, which covers 80% of the costs for the remaining two appointments.

Cost of each subsequent appointment after insurance:
400×0.20=80
Total out-of-pocket for the two subsequent appointments:
80×2=160
4.Sum Up All Expenses:
Total expenses include the first appointment, the insurance payment, and the out-of-pocket costs for the remaining appointments:
400+100+160=660

The answer is 660.

Q:{Question}

{Hints}

A:
'''




if __name__ == "__main__":
    # load data
    questions,groundTruth = data_reader("gsm8k","../data/gsm8k/test.jsonl")
    
    preds = []
    preds_ans = []

    with open("../secret.json", 'r') as f:
        data = json.load(f)

    
    itf = TextInterface(
        model="gpt-4o-mini",
        task_name="mgsm_en",
        api_key=data['api_key'],
        base_url=data['base_url'],
        visitType="OpenAI_compa",
        extract_answer=answer_cleaning
    )
    general_rule = "YOU ARE one of the GREATEST mathematicians, logicians, programmers, and AI scientists. You are intelligent and rational. You are prudent and cautious. Your mastery over Arithmetic, Combinatorics, Number Theory, Probability Theory, Algebra, Analysis, and Geometry is unparalleled. You THINK NATURAL, BROAD AND DEEP. Let's think step by step."
    hint_generate_rule= general_rule + "YOU will be given a mathematical question Q, and you need to generate intermediate hints to approach the answer of the given question Q. Before you begin to solve the question, you are asked to generate some hints for yourself. "
    question_generate_rule = general_rule + "Now,based from following hints that wll help for problem solving,give your final answer about the question."
    
    def hint_base_fn(question:str,itf:TextInterface = itf)->str:
        # generate Hints
        hints = itf.call(hint_template.format(Question = question),temperature=0.8,meta_prompt=hint_generate_rule)
        # combine questions and hints to solve problem
        pred  = itf.call(answer_template.format(Question = question,Hints = hints),meta_prompt=question_generate_rule)
        return pred

    # #solve each problem though this method
    # for question in tqdm(questions):
        
    #     # generate Hints
    #     hints = itf.call(hint_template.format(Question = question),temperature=0.8,Rule=hint_generate_rule)
    #     # combine questions and hints to solve problem
    #     pred =  itf.call(answer_template.format(Question = question,Hints = hints),Rule=question_generate_rule)
        
    #     pred_ans = itf.extract_answer(pred)
    #     preds.append(pred)
    #     preds_ans.append(pred_ans)
    
    filepath = getPredAndWrite(itf,questions[:2],groundTruth[:2],hint_base_fn,begin=0)
    
    