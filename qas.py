#!/usr/bin/python3

# Prueba de Concepto de un "Question Answering System" utilizando BERT y Google Search.
# Se probaran 30 preguntas. 10 fácticas simples, 10 fácticas complejas y 10 no fácticas
# para calcular la precisión con cada tipo de pregunta utilizando este modelo.
# Autor: Ashuin Sharma
# Universidad de Costa Rica

import torch
import sys
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
from pathlib import Path

def read_db():
    txt = Path('db.txt').read_text()
    return txt


def process_question(question, answer_text):
    input_ids = tokenizer.encode(question, answer_text)
    # BERT only needs the token IDs, but for the purpose of inspecting the
    # tokenizer's behavior, let's also get the token strings and display them.
    tokens = tokenizer.convert_ids_to_tokens(input_ids)
    # Search the input_ids for the first instance of the `[SEP]` token.
    sep_index = input_ids.index(tokenizer.sep_token_id)
    # The number of segment A tokens includes the [SEP] token istelf.
    num_seg_a = sep_index + 1
    # The remainder are segment B.
    num_seg_b = len(input_ids) - num_seg_a
    # Construct the list of 0s and 1s.
    segment_ids = [0] * num_seg_a + [1] * num_seg_b
    # Run our example through the model.
    outputs = model(torch.tensor([input_ids]),  # The tokens representing our input text.
                    token_type_ids=torch.tensor([segment_ids]),
                    # The segment IDs to differentiate question from answer_text
                    return_dict=True)
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)
    # Combine the tokens in the answer and print it out.
    # Start with the first token.
    answer = tokens[answer_start]
    # Select the remaining answer tokens and join them with whitespace.
    for i in range(answer_start + 1, answer_end + 1):
        # If it's a subword token, then recombine it with the previous token.
        if tokens[i][0:2] == '##':
            answer += tokens[i][2:]
        # Otherwise, add a space then the token.
        else:
            answer += ' ' + tokens[i]
    return answer


def retrieve_base_answer_text(question):
    return read_db()


def process_batch_questions(questions_file_path):
    load_bert()
    files = questions_file_path.split(',')
    for path in files:
        file = open(path, 'r')
        outputpath = path.replace('.qst', '') + "_answers.txt"
        outputfile = open(outputpath, 'w')
        lines = file.readlines()
        count = 0
        # Strips the newline character
        for line in lines:
            count += 1
            question = line.strip()
            print("Pregunta{}: {}".format(count, question))
            base_answer_text = retrieve_base_answer_text(question)
            answer = process_question(question, base_answer_text)
            outputfile.write(answer+'\n')
            print("Respuesta{}: {}".format(count, answer))
        file.close()
        outputfile.close()


def load_bert():
    global model, tokenizer
    model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')


def single_question(question):
    load_bert()
    answer_text = retrieve_base_answer_text(question)
    print(f'Pregunta ingresada: {question}')
    ans = process_question(question, answer_text)
    print('Respuesta: "' + ans + '"')
    return ans


def single_question_bot(question):
    if question != '/start':
        answer_text = retrieve_base_answer_text(question)
        ans = process_question(question, answer_text)
        print('Question answered..')
        return ans
    else:
        return "Hi there! ask me something.."


def ask_questions():
    load_bert()
    keep = 's'
    while keep != 'n':
        print('QAS - Ingrese una pregunta : ')
        keyboard = input()
        answer_text = retrieve_base_answer_text(keyboard)
        ans = process_question(keyboard, answer_text)
        print('Respuesta: "' + ans + '"')
        print('---')
        keep = ''
        while keep.lower() not in ['s', 'n']:
            print('Quieres continuar? (s/n) :')
            keep = input()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg.endswith('.qst'):
            process_batch_questions(arg)
        else:
            single_question(arg)
    else:
        ask_questions()
