#!/bin/bash

start_time=$(date +%s)

# Exit on error
set -e

# Set debug
set -x

# Uppdatera systemet med alla säkerhetsuppdateringar och uppgradera alla paket
echo "Updating and upgrading system with security updates..."
sudo apt update -y && sudo apt upgrade -y && sudo apt dist-upgrade -y

# Installera Git
echo "Installing git"
sudo apt install git -y

# Sätt upp git namn och e-post
echo "Setting up git name and email"
git config --global user.name "bappelberg"
git config --global user.email "benjamin.w.appelberg@gmail.com"
# Installera Vim (eller en annan editor som du föredrar)
echo "Installing Vim"
sudo apt install vim -y
echo "making vim git core editor"
git config --global core.editor "vim"
git config --global --get core.editor
# Installera OpenSSH-server
echo "Installing OpenSSH-server"
sudo apt install openssh-server -y

# Installera OpenSSH-client
echo "Installing OpenSSH-client"
sudo apt install openssh-client -y

# Om ~/.ssh finns, ta bort den
if [[ -d ~/.ssh ]]; then
    echo "Removing ~/.ssh directory"
    sudo rm -rf ~/.ssh
fi

# Skapa ~/.ssh katalog och konfigurera rätt behörigheter
echo "Creating ~/.ssh directory and configure correct permissions"
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Generera SSH nyckel-paret
echo "Generating ssh key-value pair"
ssh-keygen -t ed25519 -C "benjamin.w.appelberg@gmail.com" -f ~/.ssh/id_ed25519 -N ""

# Starta ssh-agent och lägg till nyckeln
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Visa publik SSH nyckel och ge instruktioner
cat ~/.ssh/id_ed25519.pub
echo "Go to https://github.com/settings/keys and add your ~/.ssh/id_ed25519.pub SSH key"

# Installera cURL
echo "Installing cURL"
sudo apt install curl -y

# Installera Java (OpenJDK 17)
echo "Installing Java"
sudo apt install fontconfig openjdk-17-jre -y

# Lägg till Jenkins repository och installera Jenkins
echo "Installing Jenkins"
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update -y
sudo apt install jenkins -y

# Kontrollera Jenkins status
echo "To check Jenkins status run: sudo systemctl status jenkins"

# Kontrollera Jenkins loggar
echo "Debug Jenkins logs: sudo journalctl -u jenkins --no-pager -n 50"

# Säkerställ att Jenkins startar vid systemstart
echo "Ensuring Jenkins starts on boot: sudo systemctl enable jenkins"

# Testa Jenkins om den startade korrekt
echo "If active failed: sudo systemctl restart jenkins"

# Installera build-essential (vanliga utvecklingsverktyg)
echo "Installing build-essential"
sudo apt install build-essential -y

# Installera nödvändiga beroenden för docker
sudo apt install -y ca-certificates gnupg lsb-release


# Installera Python3 och pip
echo "Installing Python3"
sudo apt install python3 python3-pip -y

# Installera Docker
echo "Installing Docker"
sudo apt install docker.io -y



# Installera htop för systemövervakning
echo "Installing htop for system monitoring"
sudo apt install htop -y

sudo apt install nginx -y

# Ta bort onödiga paket och rensa systemet
echo "Removing unnecessary packages and cleaning up"
sudo apt autoremove -y
sudo apt clean


echo "Setting git branch colors"
echo 'parse_git_branch() {
     git branch 2> /dev/null | sed -e "/^[^*]/d" -e "s/* \(.*\)/(\1)/"
}
export PS1="\u@\h \[\e[32m\]\w \[\e[91m\]\$(parse_git_branch)\[\e[00m\]$ "' >> ~/.bashrc

source ~/.bashrc
end_time=$(date +%s)

elapsed_time=$((end_time - start_time))
echo "Setup is done. Elapsed time: $elapsed_time seconds"

# Testa och verifiera installationer
echo "Verifying installations"
git --version
java -version
echo "Check jenkins status: sudo systemctl status jenkins"
echo "END OF PROGRAM"
