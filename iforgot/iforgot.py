import sys
import os

dir = os.path.dirname(__file__)
RULES_PATH = dir+'/rules.txt'
RULES_FLAG = "RULES"


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
                self.essentials.append([k.strip() for k in self.keywords[i].split("/")])
        self.cmd = command
        self.flags = []
        self.args = []
        for i in xrange(len(self.cmd)):
            open_loc = self.cmd[i].find("<")
            close_loc = self.cmd[i].find(">")
            if open_loc!=-1 and close_loc!=-1:
                flag = self.cmd[i][open_loc+1:close_loc]
                if flag==RULES_FLAG:
                    self.cmd[i] = RULES_PATH
                else:
                    flag_detail = flag.split(":")
                    flag_options = flag_detail[0].split("/")
                    for f in flag_options:
                        self.flags.append(
                            (f, self.cmd[i][:open_loc], self.cmd[i][close_loc+1:])
                        )
                        self.args += [i]
                    if len(flag_detail)>1:
                        flag_description = flag_detail[-1]
                        self.cmd[i] = "<"+flag_description+">"

    def score(self, prompt):
        for ess in self.essentials:
            found = False
            for e in ess:
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
                if p == self.flags[j][0]:
                    ns = (self.keywords+[item for sublist in self.essentials for item in sublist])
                    if len(prompt)>i+1 and prompt[i+1] not in ns:
                        cmd[self.args[j]] = self.flags[j][1] + prompt[i+1] + self.flags[j][2]
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
    # fix quotes
    newargs = []
    acc_arg = ""
    adding = False
    for arg in args:
        if arg[0]=="\"":
            acc_arg += arg
            adding = True
        if arg[-1]=="\"":
            newargs.append(acc_arg)
            acc_arg = ""
            adding = False
        if adding:
            acc_arg += " " + arg
        else:
            newargs.append(arg)
    if len(args)>0:
        check(newargs)
    else:
        print("usage: iforgot <prompt>")
        print("example:")
        print(">>iforgot how to change my MAC address to aa:bb:cc:dd")
        print("Possible matches:")
        print("spoof set aa:bb:cc:dd <on>")