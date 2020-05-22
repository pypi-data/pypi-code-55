# -*- coding:utf-8 -*-

import os
from subprocess import call
from .igen import IGen


class VIMGen(IGen):

    def generate(self, name):
        contents = r'''
filetype plugin indent on
let mapleader="\<space>"
syntax enable
syntax on

" {{{ Plugin Manager
call plug#begin('~/.vim/plugged')

 " LOOK and FEEL
 "Plug 'vim-airline/vim-airline'
 "Plug 'vim-airline/vim-airline-themes'
 "Plug 'liuchengxu/eleline.vim'
 Plug 'itchyny/lightline.vim'
 Plug 'luochen1990/rainbow'
 Plug 'yonchu/accelerated-smooth-scroll'
 Plug 'MarcWeber/vim-addon-mw-utils'

 " CODING
 Plug 'neoclide/coc.nvim',{'branch': 'release'}
 Plug 'honza/vim-snippets'
 Plug 'scrooloose/nerdcommenter'
 Plug 'skywind3000/asynctasks.vim'
 Plug 'skywind3000/asyncrun.vim'
 Plug 'puremourning/vimspector'

 " File Navigation
 Plug 'Shougo/defx.nvim'
 Plug 'roxma/nvim-yarp'
 Plug 'roxma/vim-hug-neovim-rpc'
 Plug 'kristijanhusak/defx-icons'
 Plug 'Yggdroot/LeaderF'

call plug#end()
" }}}

" {{{ SPECTOR
let g:vimspector_enable_mappings = 'VISUAL_STUDIO'
map <leader>d :VimspectorReset<CR>
sign define vimspectorBP text= texthl=Normal
sign define vimspectorBPDisabled text= texthl=Normal
"sign define vimspectorPC text= texthl=SpellBad
"sign define vimspectorPC text= texthl=SpellBad
sign define vimspectorPC text= texthl=SpellBad
" }}}

" {{{ ASYNCTASKS
let g:asyncrun_open = 6
let g:asyncrun_rootmarks = ['.root']
"let g:asynctasks_term_pos = 'bottom'
noremap <leader>r :AsyncTask project-run<CR>
noremap <leader>i :AsyncTask project-build<CR>
map <leader>x :ccl<CR>
" }}}

" {{{ DEFX
call defx#custom#option('_',{
  \ 'winwidth':23,
  \ 'split': 'vertical',
  \ 'direction': 'topleft',
  \ 'show_ignored_files': 0,
  \ 'buffer_name':'defx',
  \ 'toggle': 1,
  \ 'resume': 1
  \})
function QuitIfOnlyDefxLeft()
   if exists("g:loaded_defx")
        if bufname() == "[defx] defx-0"
            if winnr("$") == 1
                q
            endif
        endif
    endif
endfunction
autocmd WinEnter * call QuitIfOnlyDefxLeft()
map <leader>; :Defx  -columns=mark:indent:icons:filename:type<CR>
autocmd FileType defx call s:defx_mappings()
function! s:defx_mappings() abort
  nnoremap <silent><buffer><expr> o  <SID>defx_toggle_tree() 
  nnoremap <silent><buffer><expr> .  defx#do_action('toggle_ignored_files')
  nnoremap <silent><buffer><expr> r  defx#do_action('redraw')
  nnoremap <silent><buffer><expr> U  defx#do_action('cd', ['..'])
  nnoremap <silent><buffer><expr> ~  defx#do_action('cd')
  nnoremap <silent><buffer><expr> >  defx#do_action('resize', defx#get_context().winwidth + 5)
  nnoremap <silent><buffer><expr> <  defx#do_action('resize', defx#get_context().winwidth - 5)
  nnoremap <silent><buffer><expr> n  defx#do_action('new_file')
  nnoremap <silent><buffer><expr> N  defx#do_action('new_directory')
  nnoremap <silent><buffer><expr> d  defx#do_action('remove')
  nnoremap <silent><buffer><expr> c  defx#do_action('rename')
  nnoremap <silent><buffer><expr> y  defx#do_action('copy')
  nnoremap <silent><buffer><expr> p  defx#do_action('paste')
  nnoremap <silent><buffer><expr> m  defx#do_action('move')
endfunction
function! s:defx_toggle_tree() abort
    if defx#is_directory()
        return defx#do_action('open_or_close_tree')
    endif
    return defx#do_action('multi', ['drop'])
endfunction
autocmd BufWritePost * call defx#redraw()
"call defx#custom#option('_', { 'root_marker': '[PROJ] ==> ' })
"call defx#custom#option('_', { 'root_marker': '' })
call defx#custom#option('_', { 'root_marker': '' })
call defx#custom#column('mark', {  'readonly_icon': '✗',  'selected_icon': '✓' })
function! Root(path) abort
    return fnamemodify(a:path, ":t")
endfunction
call defx#custom#source('file',{ 'root': 'Root' })
let g:defx_icons_parent_icon = ''
" }}}


" {{{ COC.NVIM
set hidden
set cmdheight=2
set signcolumn=yes
set updatetime=300
set shortmess+=c
let g:coc_global_extensions = [
    \ 'coc-prettier',
    \ 'coc-highlight',
    \ 'coc-yank',
    \ 'coc-pairs',
    \ 'coc-calc',
    \ 'coc-markdownlint',
    \ 'coc-git',
    \ 'coc-snippets',
    \ 'coc-cmake',
    \ 'coc-json',
    \ 'coc-python',
    \ 'coc-clangd',
    \ ]
function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction

inoremap <silent><expr> <TAB>
      "\ pumvisible() ? coc#_select_confirm() :
      \ pumvisible() ? "\<C-n>" :
      \ coc#expandableOrJumpable() ? "\<C-r>=coc#rpc#request('doKeymap', ['snippets-expand-jump',''])\<CR>" :
      \ <SID>check_back_space() ? "\<TAB>" :
      \ coc#refresh()

inoremap <expr><S-TAB> pumvisible() ? "\<C-p>" : "\<C-h>"
inoremap <silent><expr> <c-space> coc#refresh()

if exists('*complete_info')
  inoremap <expr> <cr> complete_info()["selected"] != "-1" ? "\<C-y>" : "\<C-g>u\<CR>"
else
  inoremap <expr> <cr> pumvisible() ? "\<C-y>" : "\<C-g>u\<CR>"
endif

let g:coc_snippet_next = '<tab>'
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)
nnoremap <silent> K :call <SID>show_documentation()<CR>

function! s:show_documentation()
  if (index(['vim','help'], &filetype) >= 0)
    execute 'h '.expand('<cword>')
  else
    call CocAction('doHover')
  endif
endfunction
autocmd CursorHold * silent call CocActionAsync('highlight')
" }}}

" {{{ Status Line
set laststatus=2
let g:lightline = { 
   \ 'colorscheme': 'wombat',
   "\ 'colorscheme': 'jellybeans',
   \ 'active' : {
   \    'left' : [ ['mode', 'paste'],
   \              ['readonly', 'filename', 'modified','cocstatus' ]],
   \    'right' : [['percent','lineinfo'],]
   \},
   \ 'component_function': {
   \     'cocstatus': 'coc#status'
   \},
   \ 'mode_map': {
     \ 'n' : 'N',
     \ 'i' : 'I',
     \ 'R' : 'R',
     \ 'v' : 'V',
     \ 'V' : 'VL',
     \ "\<C-v>" : 'VB',
     \ 'c' : 'C',
     \ 's' : 'S',
     \ "\<C-s>" : 'SB',
     \ 't' : 'T',
   \},
   \}

"let g:airline_powerline_fonts = 1
"let g:eleline_powerline_fonts = 1
"let g:eleline_slim = 1
"let g:airline_theme='bubblegum'
"let g:airline_theme='violet'
"let g:airline_theme='deus'
"let g:airline_theme='badwolf'
"let g:airline_theme='papercolor'
"let g:airline_theme='minimalist'
"let g:airline_theme='sol'
"let g:airline_theme='base16_vim'
"let g:airline_theme='soda'
"let g:airline#extensions#tabline#left_sep = ' '
"let g:airline#extensions#tabline#left_alt_sep = '|'
"let g:airline#extensions#tabline#formatter = 'default'
"set statusline^=%{coc#status()}%{get(b:,'coc_current_function','')}
" }}}

" {{{ Doxygen
let g:DoxygenToolkit_authorName="Yizi Wu, wuyz0321@hngytobacco.com"
let s:licenseTag="Copyright(C)\\"
let s:licenseTag=s:licenseTag."Yizi Wu @ hngytobacco\\"
let s:licenseTag=s:licenseTag."All rights reserved\\"
let g:DoxygenToolkit_licenseTag=s:licenseTag
let g:DoxygenTookit_briefTag_funcName="yes"
let g:doxygen_enhanced_color=1
let g:DoxygenToolkit_briefTag_pre="@brief "
let g:DoxygenToolkit_paramTag_pre="@param "
let g:DoxygenToolkit_returnTag="@returns   "
" }}}

" {{{ Rainbow
let g:rainbow_active = 1
" }}}

" {{{ System
set nocp
set fileencodings=UTF-8
set encoding=UTF-8
set termencoding=UTF-8
set nu
set nowrap
set autoread
set autowrite
set noeb
set foldmethod=syntax
set foldcolumn=3
set foldenable
set tabstop=4
set shiftwidth=4
set softtabstop=4
set autoindent
set cindent
set expandtab
set smartindent
set wildmenu
set nobackup
set nowritebackup
set noswapfile
set ruler
set cursorline
set magic
set showmatch
set matchtime=5
set splitbelow
set relativenumber
set mouse=a
set noshowmode
colorscheme desert
"highlight VertSplit ctermbg=236 ctermfg=239
highlight VertSplit ctermbg=239 ctermfg=239
"highlight EndOfBuffer ctermfg=black ctermbg=black
autocmd BufReadPost *
            \ if line("'\"") > 0 && line("'\"") <= line("$") |
            \ exe "normal g'\"" |
            \ endif
" }}}

" {{{ ShortCuts
map <leader>t :terminal ++rows=6<CR>
map <leader><leader> <C-W>w
"autocmd Filetype python map <leader>r :!python tests/test.py<CR>
"autocmd Filetype python map <leader>i :!sudo sh build.sh<CR>
function AddTemplate()
    let infor = "# -*- coding:utf-8 -*-"
    silent put! =infor
endfunction
autocmd BufNewFile *.py call AddTemplate()
" }}}

" {{{ GUI Configuration
set guifont=Source\ Code\ Pro\ Regular\ 23
highlight NonText guifg=bg
" }}}
        '''

        filename = name
        if name == '~':
            filename = os.path.expanduser('~')
            filename = os.path.join(filename, '.vimrc')
        with open(filename, 'w') as f:
            f.write(contents)
