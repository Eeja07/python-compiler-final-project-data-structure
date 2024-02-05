import re

if_inside_if_block = False
execute_flag = False
code_blocks = []
output_history = []
outputKODE = ""
variables = {}


def evaluate_expression(expression, variables):
    def precedence(operator):
        if operator in {"+", "-"}:
            return 1
        elif operator in {"*", "/"}:
            return 2
        return 0

    def shunting_yard(tokens):
        output = []
        operators = []

        for token in tokens:
            if token.isdigit() or re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", token):
                output.append(token)
            elif token in {"+", "-", "*", "/"}:
                while operators and precedence(operators[-1]) >= precedence(token):
                    output.append(operators.pop())
                operators.append(token)
            elif token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    output.append(operators.pop())
                operators.pop()

        while operators:
            output.append(operators.pop())

        return output

    def apply_operator(operator, operands):
        if operator == "+":
            return operands[0] + operands[1]
        elif operator == "-":
            return operands[0] - operands[1]
        elif operator == "*":
            return operands[0] * operands[1]
        elif operator == "/":
            return operands[0] // operands[1]

    tokens = re.findall(r"\d+|\+|\-|\*|\/|\(|\)|[a-zA-Z_][a-zA-Z0-9_]*", expression)
    postfix_tokens = shunting_yard(tokens)

    stack = []
    for token in postfix_tokens:
        if token.isdigit():
            stack.append(int(token))
        elif re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", token):
            stack.append(variables.get(token, 0))
        elif token in {"+", "-", "*", "/"}:
            operand2 = stack.pop()
            operand1 = stack.pop()
            result = apply_operator(token, [operand1, operand2])
            stack.append(result)

    return stack[0]


def evaluate_condition(condition, variables):
    try:
        parts = condition.split()
        operand1 = (
            variables.get(parts[0], 0) if parts[0] in variables else int(parts[0])
        )
        operator = parts[1]
        operand2 = (
            variables.get(parts[2], 0) if parts[2] in variables else int(parts[2])
        )
    except ValueError:
        raise ValueError(f"Invalid condition format: {condition}")

    if operator == ">":
        return operand1 > operand2
    elif operator == "<":
        return operand1 < operand2
    elif operator == ">=":
        return operand1 >= operand2
    elif operator == "<=":
        return operand1 <= operand2
    elif operator == "==":
        return operand1 == operand2
    elif operator == "!=":
        return operand1 != operand2
    else:
        raise ValueError(f"Invalid operator: {operator}")


def check_if_condition(line, variables):
    match = re.search(r"(if|jika)\s+(.*):", line, re.IGNORECASE)
    if match:
        condition = match.group(2)
        result = evaluate_condition(condition, variables)

        # print(f"Debug: Cek kondisi: {condition}, Result: {result}")
        return result
    else:
        raise ValueError(f"error: {line}")


def is_if_inside_block(code):
    return re.search(r"\b(jika|if)\b", code, re.IGNORECASE) is not None


def execute_if_block(line, variables):
    match = re.search(r"(if|jika)\s+(.*):", line, re.IGNORECASE)
    if match:
        condition = match.group(2)
        # print(f"Debug: Executing if block for condition: {condition}")
        code_blocks.append({"condition": condition, "execute_flag": True, "lines": []})
    else:
        raise ValueError(f"Invalid if statement format: {line}")

def handle_goto(label_name, lines_below_label):
    global output_history
    global execute_flag
    global outputKODE

    if label_name in labels:
        # print(f"\nDebug: Executing goto {label_name}")
        # Get the lines associated with the label
        lines_below_label = labels[label_name]

        if lines_below_label:
            # print(f"Debug goto: Lines below {label_name}: {lines_below_label}")
            # Execute the lines below the label
            for line in lines_below_label:
                outputKODE += eksekusi(line)+"\n"
                # print(f"Debug:: {line}")

                # Check if the loop should continue
                if not execute_flag:
                    break

            # Reset the execute_flag after loop completion
            execute_flag = True
    else:
        print(f"Warning: Label {label_name} not found.")


labels = {}  # Dictionary to store labels and associated lines
current_line = 0
lines_below_label = []
label_name = []

def eksekusi(code):
    global output_history
    global variables
    global execute_flag
    global if_inside_if_block
    global code_blocks
    global labels
    global current_line
    global lines_below_label
    global label_name
    global outputKODE

    outputKODE = ""  # Reset outputKODE at the beginning of the function

    if code.startswith('cetak("') and code.endswith('")'):
        if execute_flag or not if_inside_if_block:
            outputKODE += code[7:-2]
    elif code.startswith("cetak(") and code.endswith(")"):
        if execute_flag or not if_inside_if_block:
            angkaSaja = re.search(r"\((.*)\)", code)
            if angkaSaja:
                angkaSaja = angkaSaja.group(1)
                if angkaSaja.isdigit():
                    outputKODE += (
                        angkaSaja if (execute_flag or not if_inside_if_block) else ""
                    )
                elif angkaSaja in variables:
                    if variables[angkaSaja] == 0:
                        outputKODE += (
                            "Variabel tidak bernilai"
                            if (execute_flag or not if_inside_if_block)
                            else ""
                        )
                    else:
                        outputKODE += (
                            str(variables[angkaSaja])
                            if (execute_flag or not if_inside_if_block)
                            else ""
                        )
                else:
                    try:
                        result = evaluate_expression(angkaSaja, variables)
                        outputKODE += (
                            str(result)
                            if (execute_flag or not if_inside_if_block)
                            else ""
                        )
                    except ValueError as e:
                        outputKODE += f"Error evaluating expression: {str(e)}\n"
            else:
                outputKODE += "Error: Invalid expression format\n"
    elif "=" in code:
        parts = code.split("=", 1)
        if len(parts) == 2:
            var_name, nilai = map(str.strip, parts)
            try:
                variables[var_name] = evaluate_expression(nilai, variables)
            except ValueError as e:
                outputKODE += f"Error assigning variable: {str(e)}\n"
        else:
            outputKODE += "Error: Invalid assignment format\n"
    elif code.startswith("jika") and code.endswith(":"):
        result = check_if_condition(code, variables)
        if result:
            execute_if_block(code, variables)
            # outputKODE += "Kondisi Terpenuhi"
            execute_flag = True
            if_inside_if_block = True
        else:
            # outputKODE += "Kondisi tidak terpenuhi"
            execute_flag = False
            if_inside_if_block = True
    elif code.startswith('') and code.endswith(":"):
        label_name = code.strip()[:-1]  # Remove the trailing colon
        lines_below_label = []  # Reset lines_below_label
        labels[label_name] = lines_below_label  # Store the lines below the label
    
    elif code.startswith("goto"):
        label_name = code.split()[1].strip()

        # Append the line with goto to lines_below_label
        lines_below_label.append(code)

        # Handle goto
        handle_goto(label_name, lines_below_label)

    lines_below_label.append(code)
    output_history.append(outputKODE)

    # print(f"\nDebug: output {output_history}")
    # print(f"\nDebug: Lines below {label_name}: {lines_below_label}")
    

    return outputKODE
