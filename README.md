# Vim Menutrans Helper

 Menu item translations in Vim are so difficult that many native speakers don't
 know how to participate. It's difficult because it uses Vim Script rather than
 other common translation formats, and therefore requires translators to be
 familiar with Vim Script. Even for those versed in Vim script, it's hard for
 them to find the menu items scattering across many different files. Tools in
 this repository could solve the above problems.


* `vim_menutrans_scanner.py` is used to generate `menu_trans.vim.template`.
  With the command `python vim_menutrans_scanner.py <vimruntime> menu_trans.vim.template`
  under project root dictionay, you could get the `Untranslated messages`
  list and `Deleted messages` list, which tells you the messages need
  to be translated and messages need to be removed from the template.

* `vim_menutrans_merger.py` is to apply `menu_trans.vim.template` to every
  language. With the command `python vim_menutrans_merger.py menu_trans.vim.template /usr/share/vim/vim82/runtime/translationfile`
  under project root dictionary, you could generate the menu
  items template in `translationfile`.Since `vim_menutrans_merger.py` will cover
  the `translationfile`, it's not recommended to apply the command directly to
  the installed version on the system. You should apply it to the translation
  files in Source Tree, or create a copy and apply it to the copy if your want
  to revise the file on System. Untranslated items in the generated files will
  be annotated. The annotations should be removed after the translations are
  completed. There are three translation formats: `"TRANSLATION MISSING", TRANSLATION\ MISSING, TRANSLATION MISSING`. `"TRANSLATION MISSING"`
  shouldn't be dropped the quotes. `TRANSLATION\ MISSING` shouldn't be dropped
  the backslash, which excapes the blank behind it and makes "TRANSLATION" and
  "MISSING" stick together.

* `<vimruntime>`   
    + If you haven't installed Vim, just cloned the Vim official code
      repository, it's path is `projectroot/runtime/`.
    + If you have installed Vim on Windows, the default path is
      `C:\Program Files\Vim\vim82`.
    + If you have installed Vim on Linux, the default path is
      `/usr/share/vim/vim82`.
    + Other information could be found in `:help $VIMRUNTIME`.

With these tools, translators could only focus on how to translate instead of
finding translation items. The translation framework still needs to be
translated manually by someone who knows the language, but it's much easier.
