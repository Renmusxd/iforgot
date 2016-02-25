import sys
import os

dir = os.path.dirname(__file__)
RULES_PATH = dir+'/rules.txt'

ESS_SCORE = 10
KEY_SCORE = 3
FLAG_SCORE = 1
MISSING_PENALTY = 1
MATCH_CUTOFF = 0.75

VAL_PRINT = True


class Command:
    def __init__(self, keywords, command):
        '''
        Create command with keywords
        :param keywords: keywords for command
        :param command: list of arguments
        '''
        self.keywords = keywords
        self.essentials = []
        for i in xrange(len(self.keywords)):
            k = self.keywords[i]
            if k[0] == "*" and k[-1] == "*" and len(k) > 2:
                self.keywords[i] = k[1:-1]
                self.essentials.append(self.keywords[i])
        self.cmd = command
        self.flags = []
        self.args = []
        for i in xrange(len(self.cmd)):
            if self.cmd[i][0] == "<" and self.cmd[i][-1] == ">" and len(self.cmd[i]) > 2:
                self.flags += [self.cmd[i][1:-1]]
                self.args += [i]

    def score(self, prompt):
        for ess in self.essentials:
            any_of = [s.strip() for s in ess.split("/")]
            found = False
            for e in any_of:
                if e in prompt:
                    found = True
                    break
            if not found:
                return 0
        score = ESS_SCORE * len(self.essentials) - (len(self.keywords)*MISSING_PENALTY)
        for p in prompt:
            if p in self.keywords:
                score += KEY_SCORE
            if p in self.flags:
                score += FLAG_SCORE
        return score

    def getcmd(self, prompt):
        if type(prompt) == str:
            prompt = prompt.split()
        cmd = self.cmd[:]
        i = 0
        while i < len(prompt):
            p = prompt[i]
            for j in xrange(len(self.flags)):
                if p == self.flags[j]:
                    if len(prompt)>i+1:
                        cmd[self.args[j]] = prompt[i+1]
                    i += 1
            i += 1
        return " ".join(cmd)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return ",".join(self.essentials)+"..."+",".join(self.keywords) + " : " + ",".join(self.cmd)


def load_until_semicolon(path=RULES_PATH):
    with open(path, "r") as f:
        s = ""
        for line in f:
            line = line.strip()
            cmt_loc = line.find('#')
            if cmt_loc>-1:
                line = line[:cmt_loc].strip()
            sc_loc = 0
            searching = True
            while -1<sc_loc<len(line) and searching:
                sc_loc = line.find(';', sc_loc+1)
                if len(line)<=1 or line[sc_loc-1]!="\\":
                    searching = False
            if sc_loc>-1:
                s += line[:sc_loc]
                yield s
                s = line[sc_loc+1:].strip()
            else:
                s += line

def load_next_rule(path=RULES_PATH):
    for text in load_until_semicolon(path):
        c_loc = text.find(":")
        if c_loc > -1:
            kwords, cmd = (text[:c_loc].strip(), text[c_loc+1:].strip())
            yield Command(kwords.split(), cmd.replace("\;",";").split())


def check(arglist):
    score_list = [ (cmd.score(arglist), cmd) for cmd in load_next_rule() ]
    sorted_list = reversed(sorted(score_list, key=lambda a: a[0]))
    pos = (cmdt for cmdt in sorted_list if cmdt[0] > 0)
    i = 0
    top_score = 0
    for cmdt in pos:
        if cmdt[0]>top_score:
            top_score = cmdt[0]
        elif cmdt[0] < MATCH_CUTOFF*top_score:
            break
        if VAL_PRINT:
            print("["+str(cmdt[0])+"]\t>> "+cmdt[1].getcmd(arglist))
        else:
            print(">> "+cmdt[1].getcmd(arglist))
        i += 1
        if i == 5:
            break
    if top_score == 0:
        print("None found, please try using some more keywords")

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args)>0:
        check(args)
    else:
        print("usage: iforgot <prompt>")
        print("example:")
        print(">>iforgot how to change my MAC address to aa:bb:cc:dd")
        print("Possible matches:")
        print("spoof set aa:bb:cc:dd <on>")