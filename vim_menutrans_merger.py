import sys
import os
import re

# Translate menu name to another language. See ":help :menutranslate".
MENUTRANS_COMMANDS = {"tmenu", "menut", "menutrans", "menutranslate"}

def make_translated_dict(translation_file, translated_dict):
    """Get the translated files' content and put it into translated_dict"""

    # Encode with "latin1", because we don't care about the correctness of 
    # non-ASCII character.
    with open(translation_file, encoding='UTF-8') as f2:
        for line_number, line in enumerate(f2):
            line = line.strip()

            if not line:
                continue

            # Split a line by white spaces but not backslash-escaped spaces.
            new_word_list = re.findall(r"(?:\\ |[^ \t])+", line)

            if len(new_word_list) > 1 and new_word_list[0] in MENUTRANS_COMMANDS:
                translated_dict[new_word_list[1].lower()] = (
                        line_number, translation_file, new_word_list[1], new_word_list[2])
            elif (len(new_word_list) > 1 and new_word_list[0] == "let" and 
                    new_word_list[1].startswith("g:menutrans_")):
                translated_dict[new_word_list[1].lower()] = (
                        line_number, translation_file, new_word_list[1], new_word_list[2])
            elif len(new_word_list) > 1 and new_word_list[0].startswith("g:menutrans_"):
                translated_dict[new_word_list[0].lower()] = (
                        line_number, translation_file, new_word_list[0], new_word_list[2])

def extract_translated_message(translation_file):
    """Get the translated files' content and put it into translated_dict"""

    translated_dict = {}
    make_translated_dict(translation_file, translated_dict)

    print("translation_file_messages:")
    for key in translated_dict.keys():
        print(translated_dict[key][1] + ":" + 
            str(translated_dict[key][0] + 1) + 
            ": " + translated_dict[key][2] + 
            ": " + translated_dict[key][3])


def usage():
    print("""Usage: vim_menutrans_helper.py <translation_file>

    translation_file: the menu translation file to parse, typically under
                      "$VIMRUNTIME/lang" directory.
""")

def main():
    if (not len(sys.argv) == 2 or not os.path.isfile(sys.argv[1])):
        usage()
        sys.exit(1)

    extract_translated_message(sys.argv[1])

if __name__ == "__main__":
    main()