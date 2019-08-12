import os
import json
from django.http import HttpResponse
from rest_framework.response import Response
from rbasis.views import *
from .models import *
from .serializers import *

from pathlib import Path
import glob

#***********************************************************************************
# answer to questions
#-----------------------------------------------------------------------------------
class answer(ShAPIView):
    queryset = test.objects.all()
    serializer_class = testSerializer

    def list(self, request, *args, **kwargs):
        return Response([], status=200)


    # ===================== answer api ===================== #
    def retrieve(self, request, *args, **kwargs):

        base_path = Path(__file__).parent

        quiz = []

        # ================= loop all files in datasource directory ================= #
        for filename in glob.glob(os.path.join(base_path / "../../datasource", '*.ipynb')):
            fp = open(filename, "rb")
            cont = fp.read()
            fp.close()

            cont = json.loads(cont.decode())

            question = ""
            answer = []

            # ================= make a quiz =================== #
            for cell in cont["cells"]:
                for src in cell["source"]:
                    if src.startswith("#"):
                        if question != "":
                            question = question.replace('\n', '')

                            tmp = ""

                            i = 0
                            flg = 0
                            for i in range(0, len(question)):
                                if (question[i] == ' ' or question[i] == '#') and flg == 0: continue
                                flg = 1
                                tmp += question[i]

                            question = tmp

                            quiz.append({"question": question, "answer": answer})

                        question = src
                        answer = []
                        continue
                    if question == "":
                        continue
                    answer.append(src)

            if question != "":
                question = question.replace('\n', '')

                tmp = ""

                i = 0
                flg = 0
                for i in range(0, len(question)):
                    if (question[i] == ' ' or question[i] == '#') and flg == 0: continue
                    flg = 1
                    tmp += question[i]

                question = tmp
                quiz.append({"question": question, "answer": answer})

        # =========== find answer to the question ================ //
        question = kwargs["pk"]
        res = ""

        for t_quiz in quiz:
            if question.lower().find(t_quiz["question"].lower()) != -1 or t_quiz["question"].lower().find(question.lower()) != -1:
                for t_ans in t_quiz["answer"]:
                    res += t_ans
                    #res += "\n"

                fp = open("answer", "w")
                fp.write(res)
                fp.close()
                return Response({"answer": res}, status=200)

        return Response({"answer" : ""}, status=200)