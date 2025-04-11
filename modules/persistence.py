from typing import List
from dataclasses import dataclass, field
import json


@dataclass
class QuizQuestion:
   question: str
   correctAnswer: str
   wrongAnswers: List[str]
   timeout: int = field(default=15)
   
   def __repr__(self):
      return self.question

def load_quiz(filename):
    with open(filename, 'r') as file:
        quizDicts = json.load(file)
        questionList = []
        for q in quizDicts["listOfQuestions"]:
            qq = QuizQuestion(**q)
            questionList.append(qq)
        titleofquiz = quizDicts["title"]
    return questionList, titleofquiz