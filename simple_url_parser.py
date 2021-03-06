from __future__ import print_function
from transition_table import table
from simple_url_lexer import SimpleUrlLexer


class SimpleUrlParser(object):
    def __init__(self, output_lexer):
        self.output_lexer = output_lexer
        self.non_terminals = [
            "url", "httpaddress", "httpaddress1", "httpaddress2", "ftpaddress",
            "telnetaddress", "mailtoaddress", "login", "login1", "hostport",
            "hostport1", "hostname", "hostname1", "port", "path", "path1", "search",
            "search1", "user", "password", "segment", "xalphas", "xalphas1",
            "xalpha", "digits", "digits1", "alpha", "digit"
        ]
        self.error_position = []
        self.output = {}
        self.result = ""

    def parse(self):
        self.output = {}
        self.result = ""
        self.error_position = []
        run = 0
        stack = ["$"]

        if self.output_lexer[0].value in table["url"]:
            rule = table["url"][self.output_lexer[0].value].split(' ')

            for i in rule[::-1]:
                stack.append(i)
        else:
            self.error_position.append(self.output_lexer[0])
            return 0

        index = 0
        while True:
            run = run + 1
            action = None
            last_stack = stack.pop()

            # non-terminal
            if last_stack in self.non_terminals:
                if self.output_lexer[index].value.isalpha():
                    token_value = "A-Z a-z"
                    if token_value in table[last_stack]:
                        rule = table[last_stack][token_value]

                        if rule == "A | .. | Z | a | .. | z":
                            stack.append(self.output_lexer[index].value)
                            action = "Rule alpha -> " + self.output_lexer[index].value
                        else:
                            rule = rule.split(' ')

                            if "epsilon" not in rule:
                                for i in rule[::-1]:
                                    stack.append(i)
                            action = "Rule " + last_stack + " -> " + " ".join(rule)
                    else:
                        action = "Rule " + token_value + "->" + self.output_lexer[index].value + "not exists"
                        self.error_position.append(self.output_lexer[index])
                        index = index + 1
                        stack.append(last_stack)

                elif self.output_lexer[index].value.isdigit():
                    token_value = "0 .. 9"
                    if token_value in table[last_stack]:
                        rule = table[last_stack][token_value]

                        if rule == "0 | .. | 9":
                            stack.append(self.output_lexer[index].value)
                            action = "Rule digit -> " + self.output_lexer[index].value
                        else:
                            rule = rule.split(' ')

                            if "epsilon" not in rule:
                                for i in rule[::-1]:
                                    stack.append(i)
                            action = "Rule " + last_stack + " -> " + " ".join(rule)
                    else:
                        action = "Rule " + token_value + " -> " + self.output_lexer[index].value + " not exists"
                        self.error_position.append(self.output_lexer[index])
                        index = index + 1
                        stack.append(last_stack)

                elif self.output_lexer[index].value in table[last_stack]:
                    rule = table[last_stack][self.output_lexer[index].value].split(' ')

                    if "epsilon" not in rule:
                        for i in rule[::-1]:
                            stack.append(i)
                    action = "Rule " + last_stack + " -> " + " ".join(rule)
                else:
                    action = "Rule " + last_stack + " -> " + self.output_lexer[index].value + " not exists"
                    self.error_position.append(self.output_lexer[index])
                    index = index + 1
                    stack.append(last_stack)

            # terminal
            else:
                if self.output_lexer[index].value == last_stack:
                    if self.output_lexer[index].value != "$":
                        index = index + 1
                    else:
                        if last_stack == "$":
                            for r in self.output_lexer:
                                for e in self.error_position:
                                    if e.lexpos == r.lexpos:
                                        r.value = "<mark>" + r.value + "</mark>"
                            self.result = "".join([r.value for r in self.output_lexer]).replace("$", "")
                            return 1
                        else:
                            self.error_position.append(self.output_lexer[index])
                            index = index + 1
                            stack.append(last_stack)
                    action = "Matched"
                else:
                    action = "Not matched, pushed back to stack"
                    self.error_position.append(self.output_lexer[index])
                    index = index + 1
                    stack.append(last_stack)

            self.output[run] = {"input": None, "rules": None, "stack": None}
            self.output[run]["input"] = [v.value for v in self.output_lexer[index:]]
            self.output[run]["stack"] = stack[:]
            self.output[run]["rules"] = action

            # for e in self.error_position:
            #     result[e.]
            # for i in self.output_lexer[index:]:
            #     print(i.value, end='')
            # print ("\nstack", stack)
            # print(self.error_position)

if __name__ == '__main__':
    lexer = SimpleUrlLexer()
    lexer.build()

    file = open('/home/pukes/Projects/SJ/SJ-Assignment/subor', 'r')
    lexer.file_lexical_analysis(file)

    parser = SimpleUrlParser(lexer.output)
    parser.parse()

    # for f in parser.error_position:
    #     print(f)