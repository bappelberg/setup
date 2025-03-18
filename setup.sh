#!/bin/bash

start_time=$(date +%s)

# Exit on error
set -e

# Set debug
set -x

# Update the package list
echo "Updating package list..."
sudo apt update -y

# Upgrade existing packages
echo "Upgrading existing packages..."
sudo apt upgrade -y

echo "Installing git"
sudo apt install git -y


echo "Setting up git name and email"
git config --global user.name "bappelberg"
git config --global user.email "benjamin.w.appelberg@gmail.com"



echo "Installing OpenSSH-server"
sudo apt install openssh-server -y

echo "Installing OpenSSH-client"
sudo apt install openssh-client -y

if [[ -d ~/.ssh ]]; then
    echo "Removing ~/.ssh directory"
    sudo rm -rf ~/.ssh
fi

echo "Creating ~/.ssh directory and configure correct permissions"
mkdir -p ~/.ssh
chmod 700 ~/.ssh


echo "Generating ssh key-value pair"
ssh-keygen -t ed25519 -C "benjamin.w.appelberg@gmail.com" -f ~/.ssh/id_ed25519

elapsed_time=$((end_time - start_time))
echo "Setup is done. Elapsed time: $elapsed_time seconds" -N ""

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

cat ~/.ssh/id_ed25519.pub
echo "go to https://github.com/settings/keys and add your ./~/.ssh/id_ed25519.pub SSH key" 

echo "Installing cURL"
sudo apt install curl -y


sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt install jenkins -y

echo "Installing Java"
sudo apt install fontconfig -y openjdk-17-jre

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))
echo "Setup is done. Elapsed time: $elapsed_time seconds"

# vim, 
