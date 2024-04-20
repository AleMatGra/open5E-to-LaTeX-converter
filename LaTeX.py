# LaTeX and text modification variables
new_line = "\n"
lNew_line = "\\\\"
tab = "    "
thin_line = "\\rule{0.49\\textwidth}{0.1mm}" + lNew_line # ! adds LaTeX new line '\\'
thick_line = "\\rule{0.49\\textwidth}{0.3mm}"

# functions that simulate common LaTeX behaviour
def bold_LARGE(text):
    return "\\textbf{\\LARGE " + text + "}" + lNew_line # ! adds LaTeX new line '\\'

def bold_large(text):
    return "\\textbf{\\large " + text + "}" + lNew_line # ! adds LaTeX new line '\\'

def bold(text):
    return "\\textbf{" + text + "}"