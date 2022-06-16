#!/user/bin/env python3
#
# Copyright 2022 Ada (Haowen) Yu <me@yuhaowen.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import re
import glob
import os
import sys

MENU_COMMANDS = {
    # Menu-related commands. See ":help creating-menus"

    # Regular menu.
    "me", "menu", "noreme", "noremenu",
    # All modes except Terminal.
    "am", "amenu", "an", "anoremenu",
    # Normal mode.
    "nme", "nmenu", "nnoreme", "nnoremenu", 
    # Operator-pending mode.
    "ome", "omenu", "onoreme", "onoremenu", 
    # Visual mode. 
    "vme", "vmenu", "vnoreme", "vnoremenu", 
    # Visual and Select mode.
    "xme", "xmenu", "xnoreme", "xnoremenu", 
    # Select mode.
    "sme", "smenu", "snoreme", "snoremenu", 
    # Insert mode.
    "ime", "imenu", "inoreme", "inoremenu", 
    # Cmdline mode.
    "cme", "cmenu", "cnoreme", "cnoremenu",
    # Terminal mode.
    "tlm", "tlmenu", "tln", "tlnoremenu", "tlu", 

    # Popup menu definition. See ":help :popup".
    "popup", "popu"
}
# Definition of tips for a menus or tools. See ":help :tmenu".
TOOLIP_COMMANDS = {"tmenu", "tm"}
# Execute a string as Ex command. See ":help :execute".
EXECUTE_COMMANDS = {"cmd =", "let cmd =", "exe", "exec", "execute"}
# Execute command silently. See ":help :silent".
SILENT_COMMANDS = {"sil", "silent", "sil!", "silent!"}
# Translate menu name to another language. See ":help :menutranslate".
MENUTRANS_COMMANDS = {"tmenu", "menut", "menutrans", "menutranslate"}

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
    # Decode with "latin1", because we don't care about the correctness of 
    # non-ASCII character
    with open(untranslation_file, encoding="latin1") as f1:
        for line_number, line in enumerate(f1):
            line = line.strip()

            # Skip the Comments
            if line.startswith('"'):
                continue
            
            # Extract content from line starts with EXECUTE_COMMANDS
            pre_end = 0
            top_string = line.split()
            if ((len(top_string) > 0 and top_string[0] in EXECUTE_COMMANDS) or 
                    (len(top_string) >= 2 and top_string[0] == "cmd" 
                    and top_string[1] == "=") or 
                    (len(top_string) >= 3 and top_string[0] == "let" 
                    and top_string[1] == "cmd" and top_string[2] == "=")):
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
            # Skip the whole line if the token after ":menu" command is "enable" or "disable"
            # because such command is not a menu definition. 
            # See ":help disable-menus" for more details.
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
                    # See ":help :menu-silent", ":help :menu-special" and 
                    # ":help :menu-script".
                    if (word_list[index] == '<silent>' or 
                            word_list[index] == '<special>' or 
                            word_list[index] == '<script>' or 
                            (word_list[index][0].isdigit() and 
                            not word_list[index - 1][0].isdigit())):
                        index += 1
                    else:
                        # A menu item under "ToolBar" is not an end-user facing 
                        # string, but just an identity to be references by 
                        # ":tmenu" command, and will be translated by another 
                        # ":tmenu" command. Therefore the menu item itself 
                        # doesn't require a translation.
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

                # Split the menu item definition by dot but backslash-escaped dot
                to_be_translated_words = []
                for match in re.finditer(r"(?:\\.|[^.])+", 
                        to_be_translated_blocks):
                    word = to_be_translated_blocks[match.start(): match.end()]

                    # :see ":help menu-separator".
                    if not (len(word) != 0 and (word[0] == '-' 
                            and word[-1] == '-')):
                        to_be_translated_words.append(word)

                for word in to_be_translated_words:
                    if len(word) > 0:
                        untranslated_dict[word.lower()] = (line_number, 
                                untranslation_file, word)
            elif word_list[0] in TOOLIP_COMMANDS:
                untranslated_dict[word_list[1].lower()] = (line_number, 
                        untranslation_file, word_list[1])
            elif word_list[0].startswith("g:menutrans_"):
                untranslated_dict[word_list[0].lower()] = (line_number, 
                        untranslation_file, word_list[0])
            elif word_list[0] == "let" and (len(word_list) > 1 and 
                    word_list[1].startswith("g:menutrans_")):
                untranslated_dict[word_list[1].lower()] = (line_number, 
                        untranslation_file, word_list[1])

    # "PopUp" is used to define popup menus. The sub menu items under "PopUp" 
    # need to be translated. But "PopUp" itself is just a placeholder string. 
    # It doesn't need translation.
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
    # non-ASCII character.
    with open(translation_file, encoding='latin1') as f2:
        for line_number, line in enumerate(f2):
            line = line.strip()

            if not line:
                continue

            # Split a line by white spaces but not backslash-escaped spaces.
            new_word_list = re.findall(r"(?:\\ |[^ \t])+", line)

            if len(new_word_list) > 1 and new_word_list[0] in MENUTRANS_COMMANDS:
                translated_dict[new_word_list[1].lower()] = (
                        line_number, translation_file, new_word_list[1])
            elif (len(new_word_list) > 1 and new_word_list[0] == "let" and 
                    new_word_list[1].startswith("g:menutrans_")):
                translated_dict[new_word_list[1].lower()] = (
                        line_number, translation_file, new_word_list[1])
            elif len(new_word_list) > 1 and new_word_list[0].startswith("g:menutrans_"):
                translated_dict[new_word_list[0].lower()] = (
                        line_number, translation_file, new_word_list[0])

def usage():
    print("""Usage: vim_menutrans_helper.py <runtime_dir> <translation_file>

    runtime_dir:      the path of Vim runtime directory. See ":help $VIMRUNTIME"
                      for more details.
    translation_file: the menu translation file to parse, typically under
                      "$VIMRUNTIME/lang" directory.
""")

def verify_menutrans(runtime_dir, translation_file):
    """Scan runtime dictionary and get newly added messages and 
    deprecated (removed) messages."""

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
    print("Untranslated messages:")
    for key in untranslated_dict.keys():
        if not key in translated_dict.keys():
            print(untranslated_dict[key][1] + ":" +  
                    str(untranslated_dict[key][0] + 1) + 
                    ": " + untranslated_dict[key][2])

    print("Deleted messages:")
    for key in translated_dict.keys():
        if not key in untranslated_dict.keys():
            print(translated_dict[key][1] + ":" + 
                str(translated_dict[key][0] + 1) + 
                ": " + translated_dict[key][2])

def main():
    if (not len(sys.argv) == 3 or not os.path.isdir(sys.argv[1]) or 
            not os.path.isfile(sys.argv[2])):
        usage()
        sys.exit(1)

    verify_menutrans(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
