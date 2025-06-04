#!/bin/bash

# Parse command line arguments
DRY_RUN=false
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

# Detect package manager
if command -v apt-get &> /dev/null; then
    # Debian/Ubuntu
    PACKAGE_MANAGER="apt-get"
    UPDATE_CMD="sudo apt-get update"
    INSTALL_CMD="sudo apt-get install -y"
elif command -v dnf &> /dev/null; then
    # Fedora
    PACKAGE_MANAGER="dnf"
    UPDATE_CMD="sudo dnf update -y"
    INSTALL_CMD="sudo dnf install -y"
elif command -v yum &> /dev/null; then
    # RHEL/CentOS
    PACKAGE_MANAGER="yum"
    UPDATE_CMD="sudo yum update -y"
    INSTALL_CMD="sudo yum install -y"
else
    echo "Unsupported Linux distribution"
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

# Update package lists
echo "Updating package lists..."
run_command $UPDATE_CMD

# Install essential packages
echo "Installing essential packages..."
if [ "$DRY_RUN" = true ]; then
    echo "[DRY RUN] Would install packages:"
    echo "  zsh git curl wget vim tmux python3 python3-pip build-essential cmake gcc g++ make automake libssl-dev libffi-dev python3-dev ruby ruby-dev golang docker.io docker-compose htop jq lynx w3m nmap mtr tcpflow wireshark pandoc speedtest-cli"
else
    $INSTALL_CMD \
        zsh \
        git \
        curl \
        wget \
        vim \
        tmux \
        python3 \
        python3-pip \
        build-essential \
        cmake \
        gcc \
        g++ \
        make \
        automake \
        libssl-dev \
        libffi-dev \
        python3-dev \
        ruby \
        ruby-dev \
        golang \
        docker.io \
        docker-compose \
        htop \
        jq \
        lynx \
        w3m \
        nmap \
        mtr \
        tcpflow \
        wireshark \
        pandoc \
        speedtest-cli
fi

# Install Python packages
echo "Installing Python packages..."
if [ "$DRY_RUN" = true ]; then
    echo "[DRY RUN] Would install Python packages:"
    echo "  pipx virtualenv ipython httpie youtube-dl"
else
    pip3 install --user \
        pipx \
        virtualenv \
        ipython \
        httpie \
        youtube-dl
fi

# Install Rust
if ! command -v rustup &> /dev/null; then
    echo "Installing Rust..."
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would install Rust using rustup"
    else
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    fi
fi

# Install Starship
if ! command -v starship &> /dev/null; then
    echo "Installing Starship..."
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would install Starship"
    else
        curl -sS https://starship.rs/install.sh | sh
    fi
fi

# Install Hishtory
if [ ! -d "$HOME/.hishtory" ]; then
    echo "Installing Hishtory..."
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would install Hishtory"
    else
        curl https://hishtory.dev/install.py | python3 -
    fi
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

if [ "$DRY_RUN" = true ]; then
    echo "Dry run complete! No changes were made."
else
    echo "Linux package installation complete!"
fi 