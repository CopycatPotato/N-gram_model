import pickle 
import random
import sys
import argparse
import os

os.system('cls')

parser = argparse.ArgumentParser()

parser.add_argument("--model", action = "store", required = True)
parser.add_argument("--input-dir", action = "store")
parser.add_argument("-N", action = "store", type = int, default = 3, help = "N of the current N-gram model (default: 3)")
args = vars(parser.parse_args())

stdin = sys.stdin

class TextTrainer:
    def __init__(self, N):
        self.model = []
        self.n = N if N else 3
        self.freqs = {}
        self.splitted_text = []
        
    def prepare_text(self, text):
        new_text = " "
        for i in text.lower().replace('\n', ' '):
            n = ord(i)
            if (n >= 97 and n <= 122) or (n >= 1072 and n <= 1103) or n == 1105 or i in '-\'':
                new_text += i
            elif i == ' ' and new_text[-1] != ' ':
                new_text += i
            elif i in "!.?,;:":
                if new_text[-1] != " ":
                    new_text += " "
                new_text += i
        return new_text
    
    def fit(self, dir_path, in_text = ""):
        files = []
        text = ""
        
        if dir_path:
            for obj in os.listdir(dir_path):
                obj_path = os.path.join(dir_path, obj)
                if os.path.isfile(obj_path):
                    files.append(obj_path)
                    
            for current_text in files:
                file = open(current_text, 'r')
                text += self.prepare_text(file.read()) + " $ "
                file.close()            
        else:
            text = self.prepare_text(in_text)
            
        splitted_text = text.split(" ")
        
        for word in splitted_text:
            if word != '':
                self.splitted_text.append(word)
        self.text = text
        
        self.analyze_text()
        
        for word_index in range(self.n - 1, len(self.splitted_text)):
            self.model.append(self.get_probability(word_index))
    
    def save(self, path):
        file = open(path, "wb")
        pickle.dump(self.model, file)
        file.close()
    
    def analyze_text(self):
        prefixes = [''] * self.n
        freqs = {}
        for word in self.splitted_text:
            if word == '$':
                prefixes = [''] * self.n
                continue
            for prefix in range(0, self.n):
                prefixes[prefix] += ' ' + word
                cnt = prefixes[prefix].count(' ')
                if cnt > self.n - prefix:
                    prefixes[prefix] = ' ' + ' '.join(prefixes[prefix].split()[1:])
                    cnt -= 1
            
                if cnt == self.n - prefix:
                    str_prefix = prefixes[prefix]
                    if str_prefix not in freqs:
                        freqs[str_prefix] = 0
                    freqs[str_prefix] += 1
        self.freqs = freqs
        
    def get_probability(self, index):
        prefixes = [None] * (self.n - 1)
        probs = [None] * self.n
        splitted_text = self.splitted_text
        probs[0] = splitted_text[index]
        freqs = self.freqs
        for c in range(0, self.n - 1):
            prefix = ' '.join(splitted_text[index - self.n + 1 + c : index])
            prefixes[c] = prefix
            pprefix = ' ' + prefix
            try:
                probs[c + 1] = freqs[pprefix + ' ' + splitted_text[index]] / freqs[pprefix]
            except:
                probs[c + 1] = 0
        return [prefixes, probs]

model = TextTrainer(args["N"])

dirc = args["input_dir"]
text = ""
if not(dirc):
    print("Введите текст: \n")
    for line in stdin:
        if line == "":
            break
        text += line

print("Модель начала обучение...\n")

model.fit(dirc, text)

print("Модель закончила обучение! Идёт сохранение в файл...\n")

model.save(args["model"])

print(f"Модель сохранена: {args['model']}\n")
