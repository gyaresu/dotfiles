# Dotfiles

This repository contains my personal dotfiles and configuration files for macOS and Linux systems.

## Features

- ZSH configuration with Oh My Zsh
- Vim configuration
- Tmux configuration
- Git configuration
- SSH configuration
- Custom scripts and utilities
- Hishtory shell history

## Installation

### Prerequisites

- Git
- ZSH
- Python 3
- Ruby (for some utilities)
- Go (for some utilities)

### macOS Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dotfiles.git ~/dotfiles
   cd ~/dotfiles
   ```

2. Run the installation script:
   ```bash
   ./install.sh
   ```

   To see what would happen without making changes:
   ```bash
   ./install.sh --dry-run
   ```

3. Restart your terminal

4. Set up Hishtory:
   - Install Hishtory:
     ```bash
     curl https://hishtory.dev/install.py | python3 -
     ```
   - Initialize with your secret key:
     ```bash
     hishtory init $YOUR_HISHTORY_SECRET
     ```

### Linux Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dotfiles.git ~/dotfiles
   cd ~/dotfiles
   ```

2. Run the installation script:
   ```bash
   ./install.sh
   ```

   To see what would happen without making changes:
   ```bash
   ./install.sh --dry-run
   ```

3. Restart your terminal

4. Set up Hishtory:
   - Install Hishtory:
     ```bash
     curl https://hishtory.dev/install.py | python3 -
     ```
   - Initialize with your secret key:
     ```bash
     hishtory init $YOUR_HISHTORY_SECRET
     ```

## What Gets Installed

### macOS Packages (via Homebrew)
- Development tools (git, python, ruby, go)
- Shell utilities (zsh, tmux, starship)
- Network tools (wget, curl, nmap)
- Text editors (vim)
- And more...

### Linux Packages
- Development tools (git, python, ruby, go)
- Shell utilities (zsh, tmux, starship)
- Network tools (wget, curl, nmap)
- Text editors (vim)
- And more...

## Configuration Files

- `_zshrc`: ZSH configuration
- `_vimrc`: Vim configuration
- `_tmux.conf`: Tmux configuration
- `_gitconfig`: Git configuration
- `_ssh_config`: SSH configuration
- `_bin/`: Custom scripts and utilities

## Customization

1. Fork this repository
2. Modify the configuration files to suit your needs
3. Update the installation scripts if necessary
4. Install using the instructions above

## Troubleshooting

### Common Issues

1. **Symlink errors**: If you get permission errors during installation, make sure you have the necessary permissions in your home directory.

2. **Package installation failures**: 
   - On macOS: Make sure Homebrew is installed and up to date
   - On Linux: Make sure you have sudo privileges and your package manager is up to date

3. **Shell not changing to ZSH**:
   - Make sure ZSH is installed
   - Try running `chsh -s $(which zsh)` manually
   - Log out and log back in

4. **Hishtory not working**:
   - Make sure you've initialized it with your secret key
   - Check that the Hishtory directory exists in your home directory
   - Verify that the Hishtory configuration is being sourced in your `.zshrc`

### Getting Help

If you encounter any issues:
1. Check the troubleshooting section above
2. Look for similar issues in the repository
3. Create a new issue with:
   - Your operating system
   - The steps you followed
   - The error message you received
   - Any relevant logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Oh My Zsh](https://ohmyz.sh/)
- [Starship](https://starship.rs/)
- [Hishtory](https://hishtory.dev/)
- And all other open-source projects used in this configuration