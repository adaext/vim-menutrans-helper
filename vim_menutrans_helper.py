#!/user/bin/env python3

import re
import glob
import os
import sys

MENU_COMMANDS = {"me", "menu", "noreme", "noremenu", "am",
             "amenu", "an", "anoremenu", "nme", "nmenu",
             "nnoreme", "nnoremenu", "ome", "omenu", "onoreme",
             "onoremenu", "vme", "vmenu", "vnoreme", "vnoremenu",
             "xme", "xmenu", "xnoreme", "xnoremenu", "sme", "smenu",
             "snoreme", "snoremenu", "ime", "imenu", "inoreme", "inoremenu",
             "cme", "cmenu", "cnoreme", "cnoremenu", "tlm", "tlmenu", "tln",
             "tlnoremenu", "tunmenu", "tu", "popup", "popu"}
# Definition of tips for a menus or tools. See ":help :tmenu".
TOOLIP_COMMANDS = {"tmenu", "tm"}
# Execute a string as Ex command. See ":help :execute".
EXECUTE_COMMANDS = {"exe", "exec", "execute"}
# Execute command silently. See ":help :silent".
SILENT_COMMANDS = {"sil", "silent", "sil!", "silent!"}
TRANSLATED_MENU = {"tmenu", "menut", "menutrans", "menutranslate"}

def unescape_double_quotes(origin):
    """Strip the quotes and unescape a string inside double quotes."""

    return (origin[1:-1].replace('\\"', '"')
                        .replace("\\'", "'")
                        .replace('\\t', '\t')
                        .replace('\\\\', '\\'))

def unescape_single_quotes(origin):
    """Strip the quotes and unescape a string inside single quotes."""

    return origin[1:-1].replace("''", "'")

def extract_messages(untranslation_file, untranslated_dict):
    """Extract the messages to be translated."""
    
    # Get the untranslated files' content
    # Encode with "latin1", because we don't care about the correctness of 
    # non-english character
    with open(untranslation_file, encoding="latin1") as f1:
        for line_number, line in enumerate(f1):
            line = line.strip()

            # Skip the Comments
            if line.startswith('"'):
                continue
            
            # Extract content from line starts with EXECUTE_COMMANDS
            pre_end = 0
            top_string = line.split()
            if len(top_string) > 0 and top_string[0] in EXECUTE_COMMANDS:
                unquoted_line = ""

                # Extract content inside quotes from line
                for match in re.finditer(
                        r"'(?:''|[^'])*'|(?:\"(?:(?:\\.)|[^\"])*\")", line):
                    mid_part = line[pre_end: match.start()].strip()

                    # Add a digit, namely "5", if there are variables inside 
                    # mid_part
                    if not (mid_part == "." or mid_part == ".." or 
                            len(mid_part) == 0 or pre_end == 0):
                        unquoted_line += "5"
                    pre_end = match.end()

                    # Add current content inside quotes to unquoted_line
                    cur_part = line[match.start(): match.end()]
                    if len(cur_part) == 0:
                        continue
                    if cur_part.startswith("'"):
                        unquoted_line += unescape_single_quotes(cur_part)
                    else:
                        unquoted_line += unescape_double_quotes(cur_part)
                line = unquoted_line

            # Split line string according to blank with escaped literal blank 
            # and tab
            word_list = re.findall(r"(?:(?:\\.)|[^ \t])+", line)

            if len(word_list) == 0:
                continue
            index = 0
            # Menu_item with "disable" or enable behind MENU_COMMANDS should 
            # be ignored. See ":help :menu-disable".
            if (word_list[0] in MENU_COMMANDS and len(word_list) > 1 and 
                    (word_list[1] == "disable" or word_list[1] == "enable")):
                continue

            if word_list[0] in SILENT_COMMANDS:
                index += 1
            # Blocks needs to be translated without being split by '.'
            if index < len(word_list) and word_list[index] in MENU_COMMANDS:
                to_be_translated_blocks = ""
                index += 1
                while index < len(word_list):
                    if (word_list[index] == '<silent>' or 
                            word_list[index] == '<script>' or 
                            (word_list[index][0].isdigit() and 
                            not word_list[index - 1][0].isdigit())):
                        index += 1
                    else:
                        # Menu_item with "ToolBar" has no following words to be 
                        # translated
                        if not ("ToolBar." in word_list[index]):
                            to_be_translated_blocks = word_list[index]
                        break

                # Remove the redundant digit added at the head and tail of the 
                # mid_part
                if (len(to_be_translated_blocks) > 0 and 
                        to_be_translated_blocks[0] == '5'):
                    to_be_translated_blocks = to_be_translated_blocks[1:]
                if (len(to_be_translated_blocks) > 0 and 
                        to_be_translated_blocks[-1] == '5'):
                     to_be_translated_blocks = to_be_translated_blocks[:-1]

                if len(to_be_translated_blocks) == 0:
                    continue

                # Untranslated word string split by "." but with escaped 
                # literal dot character"\." together
                to_be_translated_words = []
                for match in re.finditer(r"(?:\\.|[^.])+", 
                        to_be_translated_blocks):
                    word = to_be_translated_blocks[match.start(): match.end()]

                    # :see ":help menu-separator".
                    if not (len(word) != 0 and (word[0] == '-' 
                            and word[-1] == '-')):
                        to_be_translated_words.append(word)

                # Conver to_be_translated_words list to string
                for word in to_be_translated_words:
                    if len(word) > 0:
                        untranslated_dict[word.lower()] = (line_number, 
                                untranslation_file, word)
            elif word_list[0] in TOOLIP_COMMANDS:
                untranslated_dict[word_list[1].lower()] = (line_number, 
                        untranslation_file, word_list[1])
            elif word_list[0] == "let" and (len(word_list) > 1 and 
                    word_list[1].startswith("g:menutrans_")):
                untranslated_dict[word_list[1].lower()] = (line_number, 
                        untranslation_file, word_list[1])

    # PopUp doesn't need to be translated
    untranslated_dict.pop("popup", None)

    # String starting and ending with '\ 'or String contains only single digit 
    # should be skipped.
    # As dictionary can't change size during iteration, 
    # to_be_deleted_untranslated_dict is to store the string should be skipped.
    to_be_deleted_untranslated_dict = {}
    for u in untranslated_dict.keys():
        if (u.startswith('\\ ') and u.endswith('\\ ')) or (len(u) == 1 and 
                u[0] >= '0' and u[0] <= '9'):
            to_be_deleted_untranslated_dict[u] = untranslated_dict[u]

    for key in to_be_deleted_untranslated_dict.keys():
        if key in untranslated_dict:
            del untranslated_dict[key]

def make_translated_dict(translation_file, translated_dict):
    """Get the translated files' content and put it into translated_dict"""

    # Encode with "latin1", because we don't care about the correctness of 
    # non-ASCII character
    with open(translation_file, encoding='latin1') as f2:
        for line_number, line in enumerate(f2):

            # List split by blank but with literal blank together per line
            new_word_list = re.findall(r"(?:\\ |[^ \t])+", line)

            if new_word_list[0] in TRANSLATED_MENU:
                translated_dict[new_word_list[1].lower()] = (
                        line_number, translation_file, new_word_list[1])

            if (new_word_list[0] == "let" and 
                    new_word_list[1].startswith("g:menutrans_")):
                translated_dict[new_word_list[1].lower()] = (
                        line_number, translation_file, new_word_list[1])
            
            if new_word_list[0] == '"NO_MENUTRANS':
                translated_dict[new_word_list[1].lower()] = (
                        line_number, translation_file, new_word_list[1])

            if (len(new_word_list) > 2 and new_word_list[0] =='"' 
                    and new_word_list[1] == "NO_MENUTRANS"):
                translated_dict[new_word_list[2].lower()] = (
                        line_number, translation_file, new_word_list[2])

def usage():
    print("""Usage: vim_menutrans_helper.py <runtime_dir> <translation_file>
            runtime_dir:the path of Vim runtime directory. 
            See ':help $VIMRUNTIME' for more details.
            translation_file: the menu translation file to parse, 
            typically under $VIMRUNTIME/lang directory.""")

def work(runtime_dir, translation_file):
    """Scan runtime dictionary and get the illegal result"""

    untranslated_dict = {}
    translated_dict = {}
    make_translated_dict(translation_file, translated_dict)

    # Traverse runtime dictionary to get the translation difference
    for file in glob.iglob(os.path.join(runtime_dir, '**', '*.vim'), 
            recursive=True):
        if (not (file.startswith(os.path.join(runtime_dir, "lang")) or 
                file.startswith(os.path.join(runtime_dir, "keymap")))):
            extract_messages(file, untranslated_dict)

    # Compare the difference between to_be_translated_set and translated_set
    print("<------", "Untranslated messages", "------>")
    for key in untranslated_dict.keys():
        if not key in translated_dict.keys():
            print(untranslated_dict[key][1] + ":" +  
                    str(untranslated_dict[key][0] + 1) + 
                    ":" + untranslated_dict[key][2])

    print("<------", "Deleted but still translated messages", "------>")
    for key in translated_dict.keys():
        if not key in untranslated_dict.keys():
            print(translated_dict[key][1] + ":" + 
                str(translated_dict[key][0] + 1) + 
                ":" + translated_dict[key][2])

def main():
    if (not len(sys.argv) == 3 or not os.path.isdir(sys.argv[1]) or 
            not os.path.isfile(sys.argv[2])):
        usage()
        sys.exit(1)
    runtime_dir = sys.argv[1]
    translation_file = sys.argv[2]
    work(runtime_dir, translation_file)

if __name__ == "__main__":
    main()
