" Of course
set nocompatible
syntax on
filetype off

" Required Vundle setup
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'
Plugin 'davidhalter/jedi-vim'
Plugin 'scrooloose/nerdtree'
Plugin 'jistr/vim-nerdtree-tabs'
"Plugin 'myusuf3/numbers.vim'
Plugin 'rodjek/vim-puppet'
Plugin 'scrooloose/syntastic'
Plugin 'godlygeek/tabular'
Plugin 'nanotech/jellybeans.vim'
Plugin 'Lokaltog/vim-powerline'
Plugin 'tpope/vim-surround'
Plugin 'elzr/vim-json'
Plugin 'chriskempson/base16-vim'
Plugin 'rizzatti/dash.vim' " https://github.com/rizzatti/dash.vim#readme
" plugin for opening header files automatically
" Simply type :AT to open up the alternate file
" (i.e., cache.h)
Plugin 'vim-scripts/a.vim'
" https://github.com/jez/vim-as-an-ide/commit/1e5757e2e76acda61d02d27af38d8c6b531cbc05
" git add                  --> :Gwrite
" git commit               --> :Gcommit
" git push                 --> :Gpush
" git checkout <file name> --> :Gread
" git blame                --> :Gblame
Plugin 'airblade/vim-gitgutter'
Plugin 'tpope/vim-fugitive'
Plugin 'Raimondi/delimitMate'
Plugin 'jez/vim-superman'
Plugin 'christoomey/vim-tmux-navigator'
Plugin 'sheerun/vim-polyglot'
"Plugin 'Valloric/YouCompleteMe'
"Plugin 'Solarized'
Plugin 'altercation/vim-colors-solarized'
Plugin 'vim-airline/vim-airline'
Plugin 'vim-airline/vim-airline-themes'
call vundle#end()
filetype plugin indent on

" --- General Settings ---

" --- Airline Themes ---
let g:airline_theme='powerlineish'
let g:airline_powerline_fonts = 1


" --- YouCompleteMe Settings ---
let g:ycm_global_ycm_extra_conf = '~/.ycm_extra_conf.py'

" ----- jez/vim-superman settings -----
" better man page support
noremap K :SuperMan <cword><CR>

" https://github.com/junegunn/fzf
set rtp+=~/.fzf

" --- delimitMate settings ---
let delimitMate_expand_cr = 1
augroup mydelimitMate
  au!
  au FileType markdown let b:delimitMate_nesting_quotes = ["`"]
  au FileType tex let b:delimitMate_quotes = ""
  au FileType tex let b:delimitMate_matchpairs = "(:),[:],{:},`:'"
  au FileType python let b:delimitMate_nesting_quotes = ['"', "'"]
augroup END

" NERDTree and NERDTree tabs
" https://github.com/jez/vim-as-an-ide/commit/b7ff90c6ca88c97398fd9457ae7ffcab41a079e9
let g:airline#extensions#tabline#enabled = 1
let g:nerdtree_tabs_open_on_console_startup = 0

" Uncomment to open tagbar automatically whenever possible
" autocmd BufEnter * nested :call tagbar#autoopen(0)

" ----- airblade/vim-gitgutter settings -----
" Required after having changed the colorscheme
hi clear SignColumn
" In vim-airline, only display "hunks" if the diff is non-zero
let g:airline#extensions#hunks#non_zero_only = 1

" Javascript Syntax
"let g:syntastic_javascript_checkers='jshint'

" --- scrooloose/syntastic settings ---
let g:syntastic_error_symbol = '✘'
let g:syntastic_warning_symbol = "▲"
augroup mySyntastic
  au!
  au FileType tex let b:syntastic_mode = "passive"
augroup END

function! ESLintArgs()
    let rules = findfile('.eslintrules', '.;')
    return rules != '' ? '--rulesdir ' . shellescape(fnamemodify(rules, ':p:h')) : ''
endfunction

autocmd FileType javascript let b:syntastic_javascript_eslint_args = ESLintArgs()

" Let's figure fuzzyfinder and it's deps out later
"Plugin 'L9'
"Plugin 'FuzzyFinder'
"Plugin 'Align'

"" START SirVer/ultisnips
 
" Track the engine.
Plugin 'SirVer/ultisnips'

" Snippets are separated from the engine. Add this if you want them:
Plugin 'honza/vim-snippets'

" Trigger configuration. Do not use <tab> if you use https://github.com/Valloric/YouCompleteMe.
let g:UltiSnipsExpandTrigger="<tab>"
let g:UltiSnipsJumpForwardTrigger="<c-b>"
let g:UltiSnipsJumpBackwardTrigger="<c-z>"

" If you want :UltiSnipsEdit to split your window.
let g:UltiSnipsEditSplit="vertical"

"" END SirVer/ultisnips

" http://learnvimscriptthehardway.stevelosh.com/chapters/10.html
" https://danielmiessler.com/blog/enhancements-to-shell-and-vim-productivity/
inoremap jk <ESC>

" https://github.com/tpope/vim-pathogen
"call pathogen#infect()

"This bellow is to support 256 color terminal with syntax highlighting
set t_Co=256

" Enable mouse in the terminal
set mouse=a

" Write the fucking file as root!!!!!!!
" cmap w!! %!sudo tee > /dev/null %

" http://ethanschoonover.com/solarized/vim-colors-solarized
set background=dark
colorscheme mustang
"colorscheme base16-default-dark
"colorscheme Solarized

" osx copy/paste
set clipboard=unnamed

" turn line numbers on
set number

" vim-powerline configs
set guifont=Menlo\ for\ Powerline:h14
let g:Powerline_symbols = 'fancy'

" With a map leader it's possible to do extra key combinations
" like <leader>w saves the current file
let mapleader = ","
let g:mapleader = ","

" Fast saving
nmap <leader>w :w!<cr>
" Fast quitting
nmap <leader>q :wq<cr>

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => VIM user interface
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Set 7 lines to the cursor - when moving vertically using j/k
set so=7

" Turn on the WiLd menu
set wildmenu

" Ignore compiled files
set wildignore=*.o,*~,*.pyc

" Always show current position
set ruler

" Height of the command bar
set cmdheight=2

" Configure backspace so it acts as it should act
set backspace=eol,start,indent
set whichwrap+=<,>,h,l

" Ignore case when searching
set ignorecase

" When searching try to be smart about cases 
set smartcase

" Highlight search results
set hlsearch

" Makes search act like search in modern browsers
set incsearch 

" Don't redraw while executing macros (good performance config)
set lazyredraw 

" For regular expressions turn magic on
set magic

" Show matching brackets when text indicator is over them
set showmatch 
" How many tenths of a second to blink when matching brackets
set mat=2

" No annoying sound on errors
set noerrorbells
set novisualbell
set t_vb=
set tm=500

" Set encoding for Vim 2025-03-26
set encoding=utf-8
set termencoding=utf-8

" Map SPACE to remove search highlighting
nmap <SPACE> <SPACE>:noh<CR>

" Commenting blocks of code.
autocmd FileType c,cpp,java,scala let b:comment_leader = '// '
autocmd FileType sh,ruby,python   let b:comment_leader = '# '
autocmd FileType conf,fstab       let b:comment_leader = '# '
autocmd FileType tex              let b:comment_leader = '% '
autocmd FileType mail             let b:comment_leader = '> '
autocmd FileType vim              let b:comment_leader = '" '
noremap <silent> ,cc :<C-B>silent <C-E>s/^/<C-R>=escape(b:comment_leader,'\/')<CR>/<CR>:nohlsearch<CR>
noremap <silent> ,cu :<C-B>silent <C-E>s/^\V<C-R>=escape(b:comment_leader,'\/')<CR>//e<CR>:nohlsearch<CR>'

" No backups. Most stuff is in git.
set nobackup
set nowb
set noswapfile

" text, tab and indent
set expandtab
set softtabstop=4 " makes the spaces feel like real tabs
set smarttab
"set shiftwidth=2
"set tabstop=2
set shiftwidth=4
set tabstop=4
set lbr
set tw=500
set ai "Auto indent
set si "Smart indent
set wrap "Wrap lines

" gyaresu added 2013-07-13 to help book writing
set linebreak
set nolist " list disables linebreak
set textwidth=0
set wrapmargin=0

" Tell vim to use an undo file
set undofile
" The directory to store the undo history
set undodir=~/.vimundo/

" moving
map j gj
map k gk

map <C-j> <C-W>j
map <C-k> <C-W>k
map <C-h> <C-W>h
map <C-l> <C-W>l

" Return to last edit position when opening files (You want this!)
autocmd BufReadPost *
     \ if line("'\"") > 0 && line("'\"") <= line("$") |
     \   exe "normal! g`\"" |
     \ endif
" Remember info about open buffers on close
set viminfo^=%

""""""""""""""""""""""""""""""
" => Status line
""""""""""""""""""""""""""""""
" Always show the status line
set laststatus=2

" Format the status line
"set statusline=\ %{HasPaste()}%F%m%r%h\ %w\ \ CWD:\ %r%{getcwd()}%h\ \ \ Line:\ %l
"set statusline=%#PmenuSel#\ %F\ %m%r%h%w\ %#LineNr#CWD:\ %r%{getcwd()}%h\ %#CursorLineNr#Line:\ %l/%L\ Col:\ %c


function! HasPaste()
    if &paste
        return 'PASTE MODE '
    else
        return ""
    endif
endfunction

" Delete trailing white space on save, useful for Python and CoffeeScript ;)
func! DeleteTrailingWS()
  exe "normal mz"
  %s/\s\+$//ge
  exe "normal `z"
endfunc

autocmd BufWrite *.py :call DeleteTrailingWS()
autocmd BufWrite *.coffee :call DeleteTrailingWS()


