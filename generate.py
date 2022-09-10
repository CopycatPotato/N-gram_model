import pickle 
import random
import sys
import argparse
import os

os.system('cls')
console_text = ""

parser = argparse.ArgumentParser()

parser.add_argument("--model", action = "store", required = True)
parser.add_argument("--prefix", action = "store")
parser.add_argument("-N", action = "store", type = int, default = 3, help = "N of the current N-gram model (default: 3)")
parser.add_argument("--length", action = "store", type = int, required = True)
args = vars(parser.parse_args())

class TextGenerator:
    def __init__(self, model_name, N):
        self.model = []
        self.length = 0
        self.n = N
        with open(model_name, 'rb') as file:
            self.model = pickle.load(file)             
    
    def generate_text(self, length, seed = None):
        self.length = length
        if not(seed):
            seed = self.get_random_word()
        seed = seed.lower()
        generated_text = seed
        self.prefix = " " + seed
        
        cnt = 0
        while cnt < length:
            self.valid_prefix()
            new_word = self.choose_word(cnt);
            generated_text += ('' if new_word == '$' else " " + new_word)
            if new_word not in ".,;:!?$":
                cnt += 1
        return generated_text
    
    def choose_word(self, cnt):
        global console_text
        
        prefix = self.prefix
        possible_words = []
        for _ in range(self.n):
            possible_words.append([])
        
        for obj in self.model:
            l = len(obj[0])
            for curr_prefix in range(0, l):
                if prefix.endswith(" " + obj[0][curr_prefix]):               
                    possible_words[curr_prefix].append([obj[1][0], obj[1][curr_prefix + 1]]) 
        ind = 0
        for obj in possible_words:
            if len(obj) != 0:
                break
            ind += 1
        words = []
        summ = 0
        for model in possible_words[ind]:                     
            words.append(model[0])   
        if words == []:
            out("Похоже, вы использовали лексику, на которой модель не обучалась, либо текст для обучения оказался слишком коротким")
            sys.exit()
        word = random.choice(words) 
        prefix += " " + word
        self.prefix = prefix
        
        out_text = console_text + "\n" + progress(cnt + 1, self.length)
        os.system('cls')
        print(out_text) 
        
        return word
    
    def valid_prefix(self):
        prefix = self.prefix
        n = self.n
        
        if prefix[-1] == " ": 
            prefix = prefix[:-1]
        splitted_prefix = prefix.split(" ")
        if len(splitted_prefix) > n - 1:
            prefix = ' '.join(splitted_prefix[1 - n:])  
        if prefix[0] != " ":
            prefix = " " + prefix 
            
        self.prefix = prefix
            
    def get_random_word(self):
        rands = []
        for obj in self.model:
            rands.append(obj[1][0])   
        rand = random.choice(rands)
        while rand in ".,?!:;":
            rand = random.choice(rands)
        return rand


def progress(curr, maxim):
    tt = (100 * curr // maxim)
    return f"[{tt // 5 * '~' + (20 - tt // 5) * ' '}] - {tt}%\n\n"

def out(text):
    global console_text
    
    print(text)
    console_text += text + "\n"
    
def format_text(text):
    out("~~~~ Итоговый текст ~~~~\n")
    
    new_text = ""
    pr = ". "
    for i in range(0, len(text) - 1):
        if pr in [". ", "! ", "? "] or pr[1] in ".!?":
            new_text += text[i].upper()
        elif not(text[i] in " \n" and text[i + 1] in "!.?;:, /n"):
            new_text += text[i]
        pr = pr[1] + text[i]
    new_text += text[-1]  + "\n"
    return new_text

out("Начинается загрузка модели из файла...\n")

model = TextGenerator(args["model"], args["N"])

out("Модель загружена, идет генерация...\n")
out(format_text(model.generate_text(args["length"], args["prefix"])))
