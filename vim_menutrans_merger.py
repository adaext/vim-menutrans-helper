import sys
import os
import re

# Translate menu name to another language. See ":help :menutranslate".
MENUTRANS_COMMANDS = {"tmenu", "menut", "menutrans", "menutranslate"}

def make_translated_dict(translation_file, translated_dict):
    """Get the translated files' content and put it into translated_dict"""

    # Encode with "latin1", because we don't care about the correctness of 
    # non-ASCII character.
    with open(translation_file, encoding='UTF-8') as f:
        for line_number, line in enumerate(f):
            line = line.strip()

            if not line:
                continue

            # Split a line by white spaces but not backslash-escaped spaces.
            new_word_list = re.findall(r"(?:\\ |[^ \t])+", line)
            match_index = [each for each in re.finditer(r"(?:\\ |[^ \t])+", line)]
            
            if len(new_word_list) > 1 and new_word_list[0] in MENUTRANS_COMMANDS:
                translated_dict[new_word_list[1].lower()] = (
                        line_number, translation_file, new_word_list[1], line[match_index[1].end():])
            elif len(new_word_list) > 1 and new_word_list[0].startswith("g:menutrans_"):
                translated_dict[new_word_list[0].lower()] = (
                        line_number, translation_file, new_word_list[0], line[match_index[0].end():])
            elif (len(new_word_list) > 1 and new_word_list[0] == "let" and 
                    new_word_list[1].startswith("g:menutrans_")):
                translated_dict[new_word_list[1].lower()] = (
                        line_number, translation_file, new_word_list[1], line[match_index[2].end():])

def extract_translated_message(template_file, translation_file):
    """Get the translated files' content and put it into translated_dict"""

    translated_dict = {}
    make_translated_dict(translation_file, translated_dict)
    replace_template_translation(template_file, translated_dict)

def replace_template_translation(template_file, translated_dict):
    """Replace the translations in template_file with the content in translated_dict"""

    newContent = ""
    # Encode with "latin1", because we don't care about the correctness of 
    # non-ASCII character.
    with open(template_file, encoding='UTF-8') as f:
        for line_number, line in enumerate(f):
            line = line.strip()
            if not line:
                newContent += "\n"
                continue

            # Split a line by white spaces but not backslash-escaped spaces.
            new_word_list = re.findall(r"(?:\\ |[^ \t])+", line)
            match_index = [each for each in re.finditer(r"(?:\\ |[^ \t])+", line)]
            hasTranslated = True
            
            if len(new_word_list) > 1 and new_word_list[0] in MENUTRANS_COMMANDS:
                if (new_word_list[1].lower() in translated_dict):
                    line = line[:match_index[1].end() + 1] + translated_dict[new_word_list[1].lower()][3]
                else:
                    hasTranslated = False
            elif len(new_word_list) > 1 and new_word_list[0].startswith("g:menutrans_"):
                if (new_word_list[0].lower() in translated_dict):
                    line = line[:match_index[0].end() + 1] + translated_dict[new_word_list[0].lower()][3]
                else:
                    hasTranslated = False
            elif (len(new_word_list) > 1 and new_word_list[0] == "let" and 
                    new_word_list[1].startswith("g:menutrans_")):
                if (new_word_list[1].lower() in translated_dict):
                    line = line[:match_index[2].end() + 1] + translated_dict[new_word_list[1].lower()][3]
                else:
                    hasTranslated = False
            
            if not hasTranslated:
                line = '" ' + line

            newContent += str(line_number + 1) + line
            newContent += "\n"

    with open("test.vim", mode="w", encoding="UTF-8") as f:
        f.write(newContent)

def usage():
    print("""Usage: vim_menutrans_helper.py <template_file> <translation_file>

    template_file: the menu translation file template, typically under 
                      "$VIM-MENUTRANS-HELPER" directory.
    translation_file: the menu translation file to parse, typically under
                      "$VIMRUNTIME/lang" directory.
""")

def main():
    if (not len(sys.argv) == 3 or not os.path.isfile(sys.argv[1])
            or not os.path.isfile(sys.argv[2])):
        usage()
        sys.exit(1)

    extract_translated_message(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()