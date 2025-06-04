# Dotfiles

My personal dotfiles configuration for both macOS and Linux systems. This repository contains configurations for various tools and applications I use daily.

## Features

- Cross-platform support (macOS and Linux)
- Zsh configuration with Oh My Zsh and Starship prompt
- Vim configuration with Vundle
- Tmux configuration
- Git configuration with OS-specific settings
- Various development tools and utilities
- Hishtory shell history
- Custom scripts and utilities

## Prerequisites

### macOS
- Homebrew (will be installed automatically if not present)
- Xcode Command Line Tools (will be installed automatically if not present)

### Linux
- A supported package manager (apt, dnf, or yum)
- sudo privileges

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/gyaresu/dotfiles.git ~/dotfiles
   cd ~/dotfiles
   ```

2. Run the installation script:
   ```bash
   # To see what would happen without making changes:
   ./install.sh --dry-run
   
   # To perform the actual installation:
   ./install.sh
   ```

The script will:
- Install required dependencies for your OS
- Create backups of existing dotfiles
- Set up symlinks to the new configurations
- Install and configure various tools

## Repository Structure

- `_bin/` - Custom scripts and utilities
- `_custom/` - Custom configurations
- `_grunt-init/` - Grunt.js templates
- `_irssi/` - IRC client configuration
- `_vim/` - Vim configuration and plugins
- `Brewfile` - Homebrew package definitions for macOS
- `install.sh` - Main installation script
- `install_linux_packages.sh` - Linux package installation script

## What Gets Installed

### Core Tools
- Zsh with Oh My Zsh
- Starship prompt
- Hishtory shell history
- Vim with Vundle
- Tmux

### Development Tools
- Python (3.9 and 3.13 on macOS, 3.x on Linux)
- Ruby with chruby
- Go
- Rust
- Docker
- Terraform
- VSCode (macOS)

### System Tools
- Various command-line utilities
- Network tools
- Development libraries

## Customization

- Place custom configurations in the `_custom` directory
- Modify the appropriate configuration files in the root directory
- Add new packages to `Brewfile` (macOS) or `install_linux_packages.sh` (Linux)

## Updating

To update your dotfiles:

```bash
cd ~/dotfiles
git pull
./install.sh
```

## Troubleshooting

If you encounter any issues:

1. Check the error messages during installation
2. Ensure you have the necessary permissions
3. Verify that all prerequisites are installed
4. Check the OS-specific configuration files

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Oh My Zsh](https://ohmyz.sh/)
- [Starship](https://starship.rs/)
- [Hishtory](https://hishtory.dev/)
- [Vundle](https://github.com/VundleVim/Vundle.vim)
- [Homebrew](https://brew.sh/)