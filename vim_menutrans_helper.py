#!/user/bin/env python3

import re
import glob

menu_commands = {"me", "menu", "noreme", "noremenu", "am",
             "amenu", "an", "anoremenu", "nme", "nmenu",
             "nnoreme", "nnoremenu", "ome", "omenu", "onoreme",
             "onoremenu", "vme", "vmenu", "vnoreme", "vnoremenu",
             "xme", "xmenu", "xnoreme", "xnoremenu", "sme", "smenu",
             "snoreme", "snoremenu", "ime", "imenu", "inoreme", "inoremenu",
             "cme", "cmenu", "cnoreme", "cnoremenu", "tlm", "tlmenu", "tln",
             "tlnoremenu", "tunmenu", "tu", "popup", "popu"}
toolbar_commands = {"tmenu", "tm"}
exe_commands = {"exe", "exec", "execute"}
sil_commands = {"sil", "silent", "sil!", "silent!"}

def unescape_double_quotes(origin):
    """Unescape double quotes."""
    return (origin.replace('\\"', '"').replace("\\'", "'").replace('\\t', '\t').replace('\\\\', '\\'))

def unescape_single_quotes(origin):
    """Unescape single quotes."""
    return origin.replace("''", "'")

def makeUnTranslatedDict(untranslated_file, untranslated_dict):
    """Get the diffence between untranslated file and translated file."""
    
    # Get the untranslated files' content
    # Encode with "latin1", because we don't care about the correctness of non-english character
    with open(untranslated_file, encoding="latin1") as f1:
        for line_number, line in enumerate(f1):
            to_be_translated_words = []

            line = line.strip()

            temp_word_list = []
            pre_end = -1
            top_string = line.split()
            if len(top_string) > 0 and top_string[0] in exe_commands:
                # Extract content inside quotes from line
                for match in re.finditer(r"'(?:''|[^'])*'|(?:\"(?:(?:\\.)|[^\"])*\")", line):
                    mid_part = line[pre_end + 1: match.start() - 1].strip()

                    # Add a digit, namely "5", if there are variables inside mid_part
                    if not ((len(mid_part) == 1 and mid_part[0] == ".") or len(mid_part) == 0 or pre_end == -1):
                        temp_word_list.append("5")
                    pre_end = match.end()
                    temp_word_list.append(line[match.start() + 1: match.end() - 1])

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
            # Split line string according to blank without backslash or tab ahead
            for match in re.finditer(r"(?:(?:\\.)|[^ \t])+", line):
                word_list.append(line[match.start(): match.end()])

            if len(word_list) == 0 or word_list[0] == '"':
                continue
            index = 0
            # Menu_item with "disable" or enable followed close behind should be ignored
            if word_list[0] in menu_commands and len(word_list) > 1 and (word_list[1] == "disable" or word_list[1] == "enable"):
                continue

            if word_list[0] in sil_commands:
                index += 1
            # Blocks needs to be translated without being splited by '.'
            if index < len(word_list) and word_list[index] in menu_commands:
                tobe_translated_blocks = ""
                index += 1
                while index < len(word_list):
                    if word_list[index] == '<silent>' or word_list[index] == '<script>' or (word_list[index][0].isdigit() and not word_list[index - 1][0].isdigit()):
                        index += 1
                    else:
                        # Menu_item with "ToolBar" has no following words to be translated
                        if not ("ToolBar." in word_list[index]):
                            tobe_translated_blocks = word_list[index]
                        break

                # Remove the redundant digit added at the head and tail of the mid_part
                if len(tobe_translated_blocks) > 0 and tobe_translated_blocks[0] == '5':
                    tobe_translated_blocks = tobe_translated_blocks[1:]
                if len(tobe_translated_blocks) > 0 and tobe_translated_blocks[-1] == '5':
                    tobe_translated_blocks = tobe_translated_blocks[:-1]

                # Menu_item with "ToolBar" constructed a tobe_translated_blocks with length equals zero
                if len(tobe_translated_blocks) == 0:
                    continue

                # Untranslated word string splitted by "."
                tobe_translated_word = tobe_translated_blocks.split('.')
                # Untranslated word string splitted by "." but with escaped literal dot character"\." together
                to_be_translated_words = []

                # Fill tobe_translated_words with '\.' together words
                pre_backlash = False
                for word in tobe_translated_word:
                    if len(word) != 0 and word[0] == '-':
                        pre_backlash = False
                        continue
                    if pre_backlash:
                        to_be_translated_words[-1] += '.' + word
                    else:
                        to_be_translated_words.append(word)
                    if len(word) != 0 and word[-1] == '\\':
                        pre_backlash = True
                    else:
                        pre_backlash = False

                # Conver tobe_translated_words list to string
                for word in to_be_translated_words:
                    if len(word) > 0:
                        untranslated_dict[word.lower()] = (line_number, untranslated_file)
            elif word_list[0] in toolbar_commands:
                untranslated_dict[word_list[1].lower()] = (line_number, untranslated_file)
            elif word_list[0] == "let" and (len(word_list) > 1 and word_list[1].startswith("g:menutrans_")):
                untranslated_dict[word_list[1].lower()] = (line_number, untranslated_file)

    # PopUp doesn't need to be translated
    untranslated_dict.pop("popup", None)

    # String starting and ending with '\ 'or String contains only single digit should be skipped.
    temp_untranslated_dict = {}
    for u in untranslated_dict.keys():
        if (u.startswith('\\ ') and u.endswith('\\ ')) or (len(u) == 1 and u[0] >= '0' and u[0] <= '9'):
            temp_untranslated_dict[u] = untranslated_dict[u]

    for key in temp_untranslated_dict.keys():
        if key in untranslated_dict:
            del untranslated_dict[key]

def makeTranslatedDict(translated_file, translated_dict):
    translated_menu = {"tmenu", "menut", "menutrans", "menutranslate"}
    # Get the translated files' content
    # Encode with "latin1", because we don't care about the correctness of non-english character
    with open(translated_file, encoding='latin1') as f2:
        for line_number, line in enumerate(f2):
            # List without '\blank' together per line
            word_list = line.split()
            if len(word_list) == 0 or word_list[0][0] == '"':
                continue

            # List with '\blank' together per line
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
                translated_dict[new_word_list[1].lower()] = (
                    line_number, translated_file)


untranslated_dict = {}
translated_dict = {}
makeTranslatedDict("runtime\lang\menu_zh_cn.utf-8.vim", translated_dict)

# Traverse runtime dictionary to get the translation difference
for file in glob.iglob("runtime/**/*.vim", recursive=True):
    if not (file.startswith("runtime\\lang\\") or file.startswith("runtime\\keymap")):
        makeUnTranslatedDict(file, untranslated_dict)

# Compare the difference between tobe_translated_set and translated_set
print("<------", "Words haven't been translated", "------>")
for key in untranslated_dict.keys():
    if not key in translated_dict.keys():
        print( untranslated_dict[key][1], ":",untranslated_dict[key][0] + 1, ":", key)
print("<------", "Words have been deleted but still in translated list", "------>")
for key in translated_dict.keys():
    if not key in untranslated_dict.keys():
        print(translated_dict[key][1],":", translated_dict[key][0] + 1,":",  key)
