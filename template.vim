" Menu Translations:	Ukrainian
" Maintainer:		Bohdan Vlasyuk <bohdan@vstu.edu.ua>
" Last Change:		11 Oct 2001
" Original translations

"
" Please, see readme at htpp://www.vstu.edu.ua/~bohdan/vim before any
" complains, and even if you won't complain, read it anyway.
"

" Quit when menu translations have already been done.
if exists("did_menu_trans")
finish
endif
let did_menu_trans = 1
let s:keepcpo= &cpo
set cpo&vim

scriptencoding utf-8

" Help menu
menutrans &Help	TRANSLATION\ MISSING
menutrans &Overview<Tab><F1>	TRANSLATION\ MISSING
menutrans &User\ Manual	TRANSLATION\ MISSING
menutrans &How-to\ links	TRANSLATION\ MISSING
"menutrans &GUI			&GIU
menutrans &Credits	TRANSLATION\ MISSING
menutrans Co&pying	TRANSLATION\ MISSING
menutrans O&rphans	TRANSLATION\ MISSING
menutrans &Version	TRANSLATION\ MISSING
menutrans &About	TRANSLATION\ MISSING

" File menu
menutrans &File	TRANSLATION\ MISSING
menutrans &Open\.\.\.<Tab>:e	TRANSLATION\ MISSING
menutrans Sp&lit-Open\.\.\.<Tab>:sp TRANSLATION\ MISSING
menutrans &New<Tab>:enew	TRANSLATION\ MISSING
menutrans &Close<Tab>:close	TRANSLATION\ MISSING
menutrans &Save<Tab>:w	TRANSLATION\ MISSING
menutrans Save\ &As\.\.\.<Tab>:sav	TRANSLATION\ MISSING
menutrans Split\ &Diff\ with\.\.\.	TRANSLATION\ MISSING
menutrans Split\ Patched\ &By\.\.\.	TRANSLATION\ MISSING
menutrans &Print	TRANSLATION\ MISSING
menutrans Sa&ve-Exit<Tab>:wqa	TRANSLATION\ MISSING
menutrans E&xit<Tab>:qa	TRANSLATION\ MISSING

" Edit menu
menutrans &Edit	TRANSLATION\ MISSING
menutrans &Undo<Tab>u	TRANSLATION\ MISSING
menutrans &Redo<Tab>^R	TRANSLATION\ MISSING
menutrans Rep&eat<Tab>\.	TRANSLATION\ MISSING
menutrans Cu&t<Tab>"+x	TRANSLATION\ MISSING
menutrans &Copy<Tab>"+y	TRANSLATION\ MISSING
menutrans &Paste<Tab>"+gP	TRANSLATION\ MISSING
menutrans Put\ &Before<Tab>[p	TRANSLATION\ MISSING
menutrans Put\ &After<Tab>]p	TRANSLATION\ MISSING
menutrans &Select\ all<Tab>ggVG	TRANSLATION\ MISSING
menutrans &Find\.\.\.	TRANSLATION\ MISSING
menutrans Find\ and\ Rep&lace\.\.\.	TRANSLATION\ MISSING
menutrans Settings\ &Window	TRANSLATION\ MISSING
menutrans &Global\ Settings	TRANSLATION\ MISSING
menutrans F&ile\ Settings	TRANSLATION\ MISSING
menutrans Toggle\ Line\ &Numbering<Tab>:set\ nu!	TRANSLATION\ MISSING
menutrans Toggle\ &List\ Mode<Tab>:set\ list!	TRANSLATION\ MISSING
menutrans Toggle\ Line\ &Wrap<Tab>:set\ wrap!	TRANSLATION\ MISSING
menutrans Toggle\ W&rap\ at\ word<Tab>:set\ lbr!	TRANSLATION\ MISSING
menutrans Toggle\ &expand-tab<Tab>:set\ et!	TRANSLATION\ MISSING
menutrans Toggle\ &auto-indent<Tab>:set\ ai!	TRANSLATION\ MISSING
menutrans Toggle\ &C-indenting<Tab>:set\ cin!	TRANSLATION\ MISSING
menutrans &Shiftwidth	TRANSLATION\ MISSING
menutrans Te&xt\ Width\.\.\.	TRANSLATION\ MISSING
menutrans &File\ Format\.\.\.	TRANSLATION\ MISSING
menutrans Soft\ &Tabstop	TRANSLATION\ MISSING
menutrans C&olor\ Scheme	TRANSLATION\ MISSING
menutrans Select\ Fo&nt\.\.\.	TRANSLATION\ MISSING


menutrans &Keymap	TRANSLATION\ MISSING
menutrans Toggle\ Pattern\ &Highlight<Tab>:set\ hls!	TRANSLATION\ MISSING
menutrans Toggle\ &Ignore-case<Tab>:set\ ic!	TRANSLATION\ MISSING
menutrans Toggle\ &Showmatch<Tab>:set\ sm!	TRANSLATION\ MISSING
menutrans &Context\ lines	TRANSLATION\ MISSING
menutrans &Virtual\ Edit	TRANSLATION\ MISSING

menutrans Never	TRANSLATION\ MISSING
menutrans Block\ Selection	TRANSLATION\ MISSING
menutrans Insert\ mode	TRANSLATION\ MISSING
menutrans Block\ and\ Insert	TRANSLATION\ MISSING
menutrans Always	TRANSLATION\ MISSING

menutrans Toggle\ Insert\ &Mode<Tab>:set\ im!	TRANSLATION\ MISSING
menutrans Search\ &Path\.\.\.	TRANSLATION\ MISSING
menutrans Ta&g\ Files\.\.\.	TRANSLATION\ MISSING


"
" GUI options
menutrans Toggle\ &Toolbar	TRANSLATION\ MISSING
menutrans Toggle\ &Bottom\ Scrollbar	TRANSLATION\ MISSING
menutrans Toggle\ &Left\ Scrollbar	TRANSLATION\ MISSING
menutrans Toggle\ &Right\ Scrollbar	TRANSLATION\ MISSING

" Programming menu
menutrans &Tools	TRANSLATION\ MISSING
menutrans &Jump\ to\ this\ tag<Tab>g^]	TRANSLATION\ MISSING
menutrans Jump\ &back<Tab>^T	TRANSLATION\ MISSING
menutrans Build\ &Tags\ File	TRANSLATION\ MISSING
" Folding
menutrans &Folding	TRANSLATION\ MISSING
menutrans &Enable/Disable\ folds<Tab>zi	TRANSLATION\ MISSING
menutrans &View\ Cursor\ Line<Tab>zv	TRANSLATION\ MISSING
menutrans Vie&w\ Cursor\ Line\ only<Tab>zMzx	TRANSLATION\ MISSING
menutrans C&lose\ more\ folds<Tab>zm	TRANSLATION\ MISSING
menutrans &Close\ all\ folds<Tab>zM	TRANSLATION\ MISSING
menutrans &Open\ all\ folds<Tab>zR	TRANSLATION\ MISSING
menutrans O&pen\ more\ folds<Tab>zr	TRANSLATION\ MISSING

menutrans Create\ &Fold<Tab>zf	TRANSLATION\ MISSING
menutrans &Delete\ Fold<Tab>zd	TRANSLATION\ MISSING
menutrans Delete\ &All\ Folds<Tab>zD	TRANSLATION\ MISSING
menutrans Fold\ column\ &width	TRANSLATION\ MISSING
menutrans Fold\ Met&hod	TRANSLATION\ MISSING
menutrans M&anual	TRANSLATION\ MISSING
menutrans I&ndent	TRANSLATION\ MISSING
menutrans E&xpression TRANSLATION\ MISSING
menutrans S&yntax	TRANSLATION\ MISSING
menutrans Ma&rker	TRANSLATION\ MISSING

" Diff
menutrans &Diff	TRANSLATION\ MISSING
menutrans &Update	TRANSLATION\ MISSING
menutrans &Get\ Block	TRANSLATION\ MISSING
menutrans &Put\ Block	TRANSLATION\ MISSING

" Make and stuff...
menutrans &Make<Tab>:make	TRANSLATION\ MISSING
menutrans &List\ Errors<Tab>:cl	TRANSLATION\ MISSING
menutrans L&ist\ Messages<Tab>:cl!	TRANSLATION\ MISSING
menutrans &Next\ Error<Tab>:cn	TRANSLATION\ MISSING
menutrans &Previous\ Error<Tab>:cp	TRANSLATION\ MISSING
menutrans &Older\ List<Tab>:cold	TRANSLATION\ MISSING
menutrans N&ewer\ List<Tab>:cnew	TRANSLATION\ MISSING
menutrans Error\ &Window	TRANSLATION\ MISSING
menutrans &Update<Tab>:cwin	TRANSLATION\ MISSING
menutrans &Close<Tab>:cclose	TRANSLATION\ MISSING
menutrans &Open<Tab>:copen	TRANSLATION\ MISSING

menutrans &Set\ Compiler	TRANSLATION\ MISSING
menutrans &Convert\ to\ HEX<Tab>:%!xxd TRANSLATION\ MISSING
menutrans Conve&rt\ back<Tab>:%!xxd\ -r TRANSLATION\ MISSING

" Names for buffer menu.
menutrans &Buffers	TRANSLATION\ MISSING
menutrans &Refresh\ menu TRANSLATION\ MISSING
menutrans Delete	TRANSLATION\ MISSING
menutrans &Alternate	TRANSLATION\ MISSING
menutrans &Next	TRANSLATION\ MISSING
menutrans &Previous	TRANSLATION\ MISSING
menutrans [No\ File]	TRANSLATION\ MISSING

" Window menu
menutrans &Window	TRANSLATION\ MISSING
menutrans &New<Tab>^Wn	TRANSLATION\ MISSING
menutrans S&plit<Tab>^Ws	TRANSLATION\ MISSING
menutrans Sp&lit\ To\ #<Tab>^W^^	TRANSLATION\ MISSING
menutrans Split\ &Vertically<Tab>^Wv	TRANSLATION\ MISSING
"menutrans Split\ &Vertically<Tab>^Wv	&Розділити\ поперек<Tab>^Wv
menutrans Split\ File\ E&xplorer	TRANSLATION\ MISSING

menutrans &Close<Tab>^Wc	TRANSLATION\ MISSING
menutrans Close\ &Other(s)<Tab>^Wo	TRANSLATION\ MISSING
menutrans Ne&xt<Tab>^Ww	TRANSLATION\ MISSING
menutrans P&revious<Tab>^WW	TRANSLATION\ MISSING
menutrans &Equal\ Size<Tab>^W=	TRANSLATION\ MISSING
menutrans &Max\ Height<Tab>^W_	TRANSLATION\ MISSING
menutrans M&in\ Height<Tab>^W1_	TRANSLATION\ MISSING
menutrans Max\ &Width<Tab>^W\|	TRANSLATION\ MISSING
menutrans Min\ Widt&h<Tab>^W1\|	TRANSLATION\ MISSING
menutrans Move\ &To	TRANSLATION\ MISSING
menutrans &Top<Tab>^WK	TRANSLATION\ MISSING
menutrans &Bottom<Tab>^WJ	TRANSLATION\ MISSING
menutrans &Left\ side<Tab>^WH	TRANSLATION\ MISSING
menutrans &Right\ side<Tab>^WL	TRANSLATION\ MISSING
menutrans Rotate\ &Up<Tab>^WR	TRANSLATION\ MISSING
menutrans Rotate\ &Down<Tab>^Wr	TRANSLATION\ MISSING

" The popup menu
menutrans &Undo	TRANSLATION\ MISSING
menutrans Cu&t	TRANSLATION\ MISSING
menutrans &Copy	TRANSLATION\ MISSING
menutrans &Paste	TRANSLATION\ MISSING
menutrans &Delete	TRANSLATION\ MISSING
menutrans Select\ &Word	TRANSLATION\ MISSING
menutrans Select\ &Line	TRANSLATION\ MISSING
menutrans Select\ &Block	TRANSLATION\ MISSING
menutrans Select\ &All	TRANSLATION\ MISSING



" The GUI toolbar
if has("toolbar")
if exists("*Do_toolbar_tmenu")
delfun Do_toolbar_tmenu
endif
fun Do_toolbar_tmenu()
tmenu ToolBar.Open	TRANSLATION MISSING
tmenu ToolBar.Save	TRANSLATION MISSING
tmenu ToolBar.SaveAll	TRANSLATION MISSING
tmenu ToolBar.Print	TRANSLATION MISSING
tmenu ToolBar.Undo	TRANSLATION MISSING
tmenu ToolBar.Redo	TRANSLATION MISSING
tmenu ToolBar.Cut	TRANSLATION MISSING
tmenu ToolBar.Copy	TRANSLATION MISSING
tmenu ToolBar.Paste	TRANSLATION MISSING
tmenu ToolBar.Find	TRANSLATION MISSING
tmenu ToolBar.FindNext	TRANSLATION MISSING
tmenu ToolBar.FindPrev	TRANSLATION MISSING
tmenu ToolBar.Replace	TRANSLATION MISSING
tmenu ToolBar.LoadSesn	TRANSLATION MISSING
tmenu ToolBar.SaveSesn	TRANSLATION MISSING
tmenu ToolBar.RunScript	TRANSLATION MISSING
tmenu ToolBar.Make	TRANSLATION MISSING
tmenu ToolBar.Shell	TRANSLATION MISSING
tmenu ToolBar.RunCtags	TRANSLATION MISSING
tmenu ToolBar.TagJump	TRANSLATION MISSING
tmenu ToolBar.Help	TRANSLATION MISSING
tmenu ToolBar.FindHelp	TRANSLATION MISSING
endfun
endif

" Syntax menu
menutrans &Syntax TRANSLATION\ MISSING
menutrans Set\ '&syntax'\ only	TRANSLATION\ MISSING
menutrans Set\ '&filetype'\ too	TRANSLATION\ MISSING
menutrans &Off	TRANSLATION\ MISSING
menutrans &Manual	TRANSLATION\ MISSING
menutrans A&utomatic	TRANSLATION\ MISSING
menutrans on/off\ for\ &This\ file	TRANSLATION\ MISSING
menutrans Co&lor\ test	TRANSLATION\ MISSING
menutrans &Highlight\ test	TRANSLATION\ MISSING
menutrans &Convert\ to\ HTML	TRANSLATION\ MISSING

" dialog texts
let menutrans_no_file = "[Немає\ Файла]"
let menutrans_help_dialog = "Вкажіть команду або слово для пошуку:\n\nДодайте i_ для команд режиму вставки (напр. i_CTRL-X)\nДодайте i_ для командного режиму (напр. с_<Del>)\nДодайте ' для позначення назви опції (напр. 'shiftwidth')"
let g:menutrans_path_dialog = "TRANSLATION MISSING"
let g:menutrans_tags_dialog = "TRANSLATION MISSING"
let g:menutrans_textwidth_dialog = "TRANSLATION MISSING"
let g:menutrans_fileformat_dialog = "TRANSLATION MISSING"

let &cpo = s:keepcpo
unlet s:keepcpo
