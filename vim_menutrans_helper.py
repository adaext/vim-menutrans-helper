# Python program to demonstrate
# sys.argv


from ast import Delete
from hashlib import new
from operator import le
import re
import glob
from xml.dom import minidom

menu_item = {"me", "menu", "noreme", "noremenu", "am",
             "amenu", "an", "anoremenu", "nme", "nmenu",
             "nnoreme", "nnoremenu", "ome", "omenu", "onoreme",
             "onoremenu", "vme", "vmenu", "vnoreme", "vnoremenu",
             "xme", "xmenu", "xnoreme", "xnoremenu", "sme", "smenu",
             "snoreme", "snoremenu", "ime", "imenu", "inoreme", "inoremenu",
             "cme", "cmenu", "cnoreme", "cnoremenu", "tlm", "tlmenu", "tln",
             "tlnoremenu", "E330", "E327", "E331", "E336", "E333", "E328", "E329",
             "E337", "E792", "tunmenu", "tu", "popup", "popu"}
toolbar_item = {"tmenu", "tm"}

# unescape double quotes


def unescape_double_quotes(origin):
    origin = origin.replace('\\"', '"')
    origin = origin.replace("\\'", "'")
    origin = origin.replace('\\t', '\t')
    origin = origin.replace('\\\\', '\\')
    return origin

# unescape single quotes


def unescape_single_quotes(origin):
    origin = origin.replace("''", "'")
    return origin

# get the diffence between untranslated file and translated file
def makeUnTranslatedDic(untranslated_file, untranslated_dict):
    # deal with the file need to be translated
    with open(untranslated_file, encoding="latin1") as f1:
        for line_number, line in enumerate(f1):
            tobe_translated_words = []

            line = line.strip()
            line = line.rstrip()

            temp_word_list = []
            pre_end = -1
            top_string = line.split()
            if len(top_string) > 0 and (top_string[0] == "exe" or top_string[0] == "exec" or top_string[0] == "execute"):
                # extract content inside quotes from line
                for ite in re.finditer(r"'(?:''|[^'])*'|(?:\"(?:(?:\\.)|[^\"])*\")", line):
                    mid_part = line[pre_end + 1: ite.start() - 1].strip()
                    if not ((len(mid_part) == 1 and mid_part[0] == ".") or len(mid_part) == 0 or pre_end == -1):
                        temp_word_list.append("5")
                    pre_end = ite.end()
                    temp_word_list.append(line[ite.start() + 1: ite.end() - 1])
                
                temp_line = ""
                for word in temp_word_list:

                    if len(word) == 0:
                        continue
                    if word[0] == "'":
                        word = unescape_single_quotes(word)
                    else:
                        word = unescape_double_quotes(word)
                    temp_line += word
                line = temp_line

            word_list = []
            # split line string according to blank without backslash or tab ahead
            for ite in re.finditer(r"(?:(?:\\.)|[^ \t])+", line):
                word_list.append(line[ite.start(): ite.end()])

            if len(word_list) == 0 or word_list[0] == '"':
                continue
            index = 0
            # menu_item with "disable" or enable followed close behind should be ignored
            if word_list[0] in menu_item and len(word_list) > 1 and (word_list[1] == "disable" or word_list[1] == "enable"):
                continue

            if word_list[0] == 'sil!':
                index += 1
            # blocks needs to be translated without being splited by '.'
            if index < len(word_list) and word_list[index] in menu_item:
                tobe_translated_blocks = ""
                index += 1
                while index < len(word_list):
                    if word_list[index] == '<silent>' or word_list[index] == '<script>' or (word_list[index][0].isdigit() and not word_list[index - 1][0].isdigit()):
                        index += 1
                    else:
                        # menu_item with "ToolBar" has no following words to be translated
                        if not ("ToolBar." in word_list[index]):
                            tobe_translated_blocks = word_list[index]
                        break

                # string starting with sill! needs to be removed first digit
                if len(tobe_translated_blocks) > 0 and tobe_translated_blocks[0] == '5':
                    tobe_translated_blocks = tobe_translated_blocks[1:]
                if len(tobe_translated_blocks) > 0 and tobe_translated_blocks[-1] == '5':
                    tobe_translated_blocks = tobe_translated_blocks[:-1]

                # menu_item with "ToolBar" constructed a tobe_translated_blocks with length equals zero
                if len(tobe_translated_blocks) == 0:
                    continue

                # untranslated word string splitted by "."
                tobe_translated_word = tobe_translated_blocks.split('.')
                # untranslated word string splitted by "." but with "\." together
                tobe_translated_words = []

                # fill tobe_translated_words with '\.' together words
                pre_backlash = False
                for word in tobe_translated_word:
                    if len(word) != 0 and word[0] == '-':
                        pre_backlash = False
                        continue
                    if pre_backlash:
                        tobe_translated_words[-1] += '.' + word
                    else:
                        tobe_translated_words.append(word)
                    if len(word) != 0 and word[-1] == '\\':
                        pre_backlash = True
                    else:
                        pre_backlash = False

                # conver tobe_translated_words list to string
                for word in tobe_translated_words:
                    if len(word) > 0:
                        untranslated_dict[word.lower()] = (line_number, untranslated_file)
            elif word_list[0] in toolbar_item:
                untranslated_dict[word_list[1].lower()] = (
                    line_number, untranslated_file)
            elif word_list[0] == "let" and (len(word_list) > 1 and word_list[1].startswith("g:menutrans_")):
                    untranslated_dict[word_list[1].lower()] = (line_number, untranslated_file)

    # PopUp doesn't need to be translated
    untranslated_dict.pop("popup", None)
            
    # blank with digit doesn't neet to be translated
    temp_untranslated_dict = {}
    for u in untranslated_dict.keys():
        if (u.startswith('\\ ') and u.endswith('\\ ')) or (len(u) == 1 and u[0] >= '0' and u[0] <= '9'):
            temp_untranslated_dict[u] = untranslated_dict[u]

    for key in temp_untranslated_dict.keys():
        if key in untranslated_dict:
            del untranslated_dict[key]

def makeTranslatedDic(translated_file, translated_dict):
    translated_menu = {"tmenu", "menut", "menutrans", "menutranslate"}
    # deal with the translated file
    with open(translated_file, encoding='utf-8') as f2:
        for line_number, line in enumerate(f2):
            # list without '\blank' together per line
            word_list = line.split()
            if len(word_list) == 0 or word_list[0][0] == '"':
                continue

            # list with '\blank' together per line
            new_word_list = []
            pre_backlash = False
            for l in word_list:
                if pre_backlash:
                    new_word_list[-1] += " " + l
                else:
                    new_word_list.append(l)
                if l[-1] == '\\':
                    pre_backlash = True
                else:
                    pre_backlash = False

            if new_word_list[0] in translated_menu:
                translated_dict[new_word_list[1].lower()] = (
                    line_number, translated_file)
            if new_word_list[0] == "let" and new_word_list[1].startswith("g:menutrans_"):
                translated_dict[new_word_list[1].lower()] = (line_number, translated_file)

untranslated_dict = {}
translated_dict = {}
makeTranslatedDic("runtime\lang\menu_zh_cn.utf-8.vim", translated_dict)
# makeUnTranslatedDic("runtime\\autoload\\netrw.vim", untranslated_dict)

# traverse runtime dictionary to get the translation difference
for file in glob.iglob("runtime/**/*.vim", recursive=True):
    if not (file.startswith("runtime\\lang\\") or file.startswith("runtime\\keymap")):
        makeUnTranslatedDic(file, untranslated_dict)

# compare the difference between tobe_translated_set and translated_set
print("<------", "Words haven't been translated", "------>")
for key in untranslated_dict.keys():
    if not key in translated_dict.keys():
        print("line:", untranslated_dict[key][0] + 1, "path:", untranslated_dict[key][1], key)

print("<------", "Words have been deleted but still in translated list", "------>")
for key in translated_dict.keys():
    if not key in untranslated_dict.keys():
        print("line:", translated_dict[key][0] + 1,"path:", translated_dict[key][1], key)