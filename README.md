# qasbert
Question Answering System using BERT developed in Python including results of applying the model to factoid, non-factoid and complex questions.
@Author Ashuin Sharma


Compilation

1- Install miniconda y python 3.10
2- conda create -n env_qas python=3.10
3- conda activate env_qas
4- conda install pytorch torchvision -c pytorch
5- conda install -c huggingface transformers
6- conda install -c conda-forge python-telegram-bot
7- conda install -c conda-forge googlesearch
8- python qas.py
9- python bot.py (To run chatbot)


File Descriptions

1- All files with .QST extensions are input files based on the type of question
2- All files with "_answer.txt" suffix are the output files with the answers.
3- allresults.txt file contains each question/answer pair sequentially.
