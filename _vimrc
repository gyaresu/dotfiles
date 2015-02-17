" https://github.com/tpope/vim-pathogen
call pathogen#infect()
set t_Co=256
syntax on
filetype plugin indent on

" Write the fucking file as root!!!!!!!
" cmap w!! %!sudo tee > /dev/null %

" http://ethanschoonover.com/solarized/vim-colors-solarized
set background=dark
colorscheme gummybears
" colorscheme monokai

" osx copy/paste
set clipboard=unnamed

" turn line numbers on
set number

" vim-powerline configs
set nocompatible
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

set encoding=utf8

" Map SPACE to remove search highlighting
nmap <SPACE> <SPACE>:noh<CR>

" No backups. Most stuff is in git.
set nobackup
set nowb
set noswapfile

" text, tab and indent
set expandtab
"set softtabstop=4 " makes the spaces feel like real tabs
set smarttab
set shiftwidth=2
set tabstop=2
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


