#!/bin/bash
############################
# install.sh
# This script creates symlinks from the home directory to any desired dotfiles in ~/dotfiles
############################

set -e  # Exit on error
set -u  # Exit on undefined variable

########## Variables
dir=~/dotfiles                    # dotfiles directory
olddir=~/dotfiles_old             # old dotfiles backup directory
DRY_RUN=false                     # dry run flag

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--dry-run]"
            exit 1
            ;;
    esac
done

# Define files to symlink based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS specific files
    files="_zshrc _vimrc _vim _tmux.conf.local _gitconfig _eslintrc _gdbinit _pastebinit.xml _irssi _grunt-init _bin _custom _ssh_config"
    darwin_files="_gitconfig.darwin"
else
    # Linux specific files
    files="_zshrc _vimrc _vim _tmux.conf.local _gitconfig _eslintrc _gdbinit _pastebinit.xml _irssi _grunt-init _bin _custom _ssh_config"
    darwin_files=""
fi

##########

# Check if we're in the correct directory
if [ ! -f "$(basename "$0")" ]; then
    echo "Error: Please run this script from the dotfiles directory"
    exit 1
fi

# Function to run commands with dry run support
run_command() {
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would run: $*"
    else
        "$@"
    fi
}

# Function to create directory with dry run support
create_dir() {
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would create directory: $1"
    else
        mkdir -p "$1"
    fi
}

# Install OS-specific dependencies
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Installing macOS dependencies..."

    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew..."
        if [ "$DRY_RUN" = true ]; then
            echo "[DRY RUN] Would install Homebrew"
        else
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
    fi

    # Install Homebrew packages
    echo "Installing Homebrew packages..."
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would run: brew bundle --file=\"$dir/Brewfile\""
    else
        brew bundle --file="$dir/Brewfile"
    fi
else
    echo "Installing Linux dependencies..."
    # Run Linux package installation script
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would run: bash \"$dir/install_linux_packages.sh\" --dry-run"
        bash "$dir/install_linux_packages.sh" --dry-run
    else
        bash "$dir/install_linux_packages.sh"
    fi
fi

# Check if zsh is installed
if ! command -v zsh &> /dev/null; then
    echo "Error: zsh installation failed. Please install zsh manually."
    exit 1
fi

# Install Oh My Zsh if not already installed
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    echo "Installing Oh My Zsh..."
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would install Oh My Zsh"
    else
        sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    fi
fi

# Install starship if not already installed
if ! command -v starship &> /dev/null; then
    echo "Installing starship..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if [ "$DRY_RUN" = true ]; then
            echo "[DRY RUN] Would run: brew install starship"
        else
            brew install starship
        fi
    else
        if [ "$DRY_RUN" = true ]; then
            echo "[DRY RUN] Would install starship"
        else
            curl -sS https://starship.rs/install.sh | sh
        fi
    fi
fi

# Install hishtory if not already installed
if [ ! -d "$HOME/.hishtory" ]; then
    echo "Installing hishtory..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if [ "$DRY_RUN" = true ]; then
            echo "[DRY RUN] Would run: brew install hishtory"
        else
            brew install hishtory
        fi
    else
        if [ "$DRY_RUN" = true ]; then
            echo "[DRY RUN] Would install hishtory"
        else
            curl https://hishtory.dev/install.py | python3 -
        fi
    fi
    echo "Note: After installation, you need to run 'hishtory init \$YOUR_HISHTORY_SECRET' to set up your hishtory account"
fi

# Set zsh as default shell if not already
if [ "$SHELL" != "$(which zsh)" ]; then
    echo "Setting zsh as default shell..."
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would run: chsh -s $(which zsh)"
    else
        chsh -s $(which zsh)
    fi
    echo "Please restart your terminal for the changes to take effect."
fi

# create dotfiles_old in homedir
echo "Creating $olddir for backup of any existing dotfiles in ~"
create_dir "$olddir"
echo "...done"

# change to the dotfiles directory
echo "Changing to the $dir directory"
cd "$dir"
echo "...done"

# Function to handle symlinks
handle_symlink() {
    local source="$1"
    local target="$2"

    # Remove leading underscore from target name
    local target_name="${target#_}"

    if [ "$DRY_RUN" = true ]; then
        if [ -e ~/."$target_name" ]; then
            echo "[DRY RUN] Would move ~/.$target_name to $olddir/"
        fi
        if [ -L ~/."$target_name" ]; then
            echo "[DRY RUN] Would remove existing symlink ~/.$target_name"
        fi
        echo "[DRY RUN] Would create symlink from $dir/$source to ~/.$target_name"
    else
        if [ -e ~/."$target_name" ]; then
            echo "Moving existing .$target_name from ~ to $olddir"
            mv ~/."$target_name" "$olddir/"
        fi
        if [ -L ~/."$target_name" ]; then
            echo "Removing existing symlink ~/.$target_name"
            rm ~/."$target_name"
        fi
        echo "Creating symlink to $target in home directory."
        ln -s "$dir/$source" ~/."$target_name"
    fi
}

# Function to handle darwin-specific files
handle_darwin_file() {
    local source="$1"
    local target="${source#_}"

    if [ "$DRY_RUN" = true ]; then
        if [ -e ~/."$target" ]; then
            echo "[DRY RUN] Would move ~/.$target to $olddir/"
        fi
        if [ -f ~/."$target" ]; then
            echo "[DRY RUN] Would remove existing file ~/.$target"
        fi
        echo "[DRY RUN] Would copy $dir/$source to ~/.$target"
    else
        if [ -e ~/."$target" ]; then
            echo "Moving existing .$target from ~ to $olddir"
            mv ~/."$target" "$olddir/"
        fi
        if [ -f ~/."$target" ]; then
            echo "Removing existing file ~/.$target"
            rm ~/."$target"
        fi
        echo "Copying $target to home directory."
        cp "$dir/$source" ~/."$target"
    fi
}

# move any existing dotfiles in homedir to dotfiles_old directory, then create symlinks
for file in $files; do
    echo "Processing $file..."
    handle_symlink "$file" "$file"
done

# Handle darwin-specific files
for file in $darwin_files; do
    echo "Processing $file..."
    handle_darwin_file "$file"
done

# Check for correct .tmux.conf symlink
if [ ! -L "$HOME/.tmux.conf" ] || [[ "$(readlink ~/.tmux.conf)" != "$HOME/.tmux/.tmux.conf" ]]; then
    echo "WARNING: ~/.tmux.conf is not symlinked to ~/.tmux/.tmux.conf"
    echo "You should run: ln -s ~/.tmux/.tmux.conf ~/.tmux.conf"
fi

# Install Vundle
echo "Installing Vundle..."
if [ "$DRY_RUN" = true ]; then
    echo "[DRY RUN] Would install Vundle"
else
    if [ ! -d "$HOME/.vim/bundle/Vundle.vim" ]; then
        git clone https://github.com/VundleVim/Vundle.vim.git "$HOME/.vim/bundle/Vundle.vim"
    fi
fi

# Install Vim plugins
echo "Installing Vim plugins..."
if [ "$DRY_RUN" = true ]; then
    echo "[DRY RUN] Would install Vim plugins"
else
    vim +PluginInstall +qall
fi

# Handle OS-specific configurations
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Setting up macOS specific configurations..."
else
    echo "Setting up Linux specific configurations..."
fi

if [ "$DRY_RUN" = true ]; then
    echo "Dry run complete! No changes were made."
else
    echo "Installation complete!"
fi
