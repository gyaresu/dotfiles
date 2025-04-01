#!/bin/bash
############################
# .make.sh
# This script creates symlinks from the home directory to any desired dotfiles in ~/dotfiles
############################

set -e  # Exit on error
set -u  # Exit on undefined variable

########## Variables
dir=~/dotfiles                    # dotfiles directory
olddir=~/dotfiles_old             # old dotfiles backup directory

# Define files to symlink based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS specific files
    files="_zshrc _vimrc _vim _tmux.conf _tmux.conf.local _gitconfig _eslintrc _gdbinit _pastebinit.xml _irssi _grunt-init _bin _custom"
    darwin_files="_gitconfig.darwin"
else
    # Linux specific files
    files="_zshrc _vimrc _vim _tmux.conf _tmux.conf.local _gitconfig _eslintrc _gdbinit _pastebinit.xml _irssi _grunt-init _bin _custom"
    darwin_files=""
fi

##########

# Check if we're in the correct directory
if [ ! -f "$(basename "$0")" ]; then
    echo "Error: Please run this script from the dotfiles directory"
    exit 1
fi

# Check if zsh is installed
if ! command -v zsh &> /dev/null; then
    echo "Installing zsh..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install zsh
    else
        sudo apt-get update
        sudo apt-get install -y zsh
    fi
fi

# Install Oh My Zsh if not already installed
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    echo "Installing Oh My Zsh..."
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi

# Install starship if not already installed
if ! command -v starship &> /dev/null; then
    echo "Installing starship..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install starship
    else
        # Download starship binary
        curl -sS https://starship.rs/install.sh | sh
    fi
fi

# Install hishtory if not already installed
if [ ! -d "$HOME/.hishtory" ]; then
    echo "Installing hishtory..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install hishtory
    else
        # Download and run hishtory installer
        curl https://hishtory.dev/install.py | python3 -
    fi
    echo "Note: After installation, you need to run 'hishtory init $YOUR_HISHTORY_SECRET' to set up your hishtory account"
fi

# Set zsh as default shell if not already
if [ "$SHELL" != "$(which zsh)" ]; then
    echo "Setting zsh as default shell..."
    chsh -s $(which zsh)
    echo "Please restart your terminal for the changes to take effect."
fi

# create dotfiles_old in homedir
echo "Creating $olddir for backup of any existing dotfiles in ~"
mkdir -p "$olddir"
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
    
    # Handle the case where the file doesn't exist
    if [ -e ~/."$target_name" ]; then
        echo "Moving existing .$target_name from ~ to $olddir"
        mv ~/."$target_name" "$olddir/"
    fi
    
    # Handle the case where the symlink already exists
    if [ -L ~/."$target_name" ]; then
        echo "Removing existing symlink ~/.$target_name"
        rm ~/."$target_name"
    fi
    
    # Create the symlink
    echo "Creating symlink to $target in home directory."
    ln -s "$dir/$source" ~/."$target_name"
}

# Function to handle darwin-specific files
handle_darwin_file() {
    local source="$1"
    local target="${source#_}"
    
    # Handle the case where the file doesn't exist
    if [ -e ~/."$target" ]; then
        echo "Moving existing .$target from ~ to $olddir"
        mv ~/."$target" "$olddir/"
    fi
    
    # Handle the case where the file already exists
    if [ -f ~/."$target" ]; then
        echo "Removing existing file ~/.$target"
        rm ~/."$target"
    fi
    
    # Copy the file instead of symlinking
    echo "Copying $target to home directory."
    cp "$dir/$source" ~/."$target"
}

# move any existing dotfiles in homedir to dotfiles_old directory, then create symlinks 
for file in $files; do
    echo "Processing $file..."
    
    # Handle directories
    if [ -d "$file" ]; then
        handle_symlink "$file" "$file"
    # Handle regular files
    elif [ -f "$file" ]; then
        handle_symlink "$file" "$file"
    else
        echo "Warning: $file not found in dotfiles directory"
    fi
done

# Handle darwin-specific files
if [[ "$OSTYPE" == "darwin"* ]]; then
    for file in $darwin_files; do
        echo "Processing darwin-specific file: $file..."
        if [ -f "$file" ]; then
            handle_darwin_file "$file"
        else
            echo "Warning: $file not found in dotfiles directory"
        fi
    done
fi

# Install Vundle Plugins
echo "Installing Vundle..."
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed. Please install git first."
    exit 1
fi

# Create .vim directory if it doesn't exist
mkdir -p ~/.vim/bundle

if [ ! -d ~/.vim/bundle/Vundle.vim ]; then
    git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
    echo "...done"
else
    echo "Vundle is already installed"
fi

# Handle OS-specific configurations
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Setting up macOS specific configurations..."
    # Add any macOS specific setup here
fi

echo "Installation complete! Please open vim and run :PluginInstall to install plugins."
echo "Note: You may need to restart your shell for all changes to take effect."

