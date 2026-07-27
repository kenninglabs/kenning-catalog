#!/bin/sh
if command -v brew >/dev/null 2>&1; then
  brew tap hashicorp/tap
  brew install hashicorp/tap/terraform
elif command -v apt >/dev/null 2>&1; then
  wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg >/dev/null
  echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
  sudo apt update && sudo apt install -y terraform
elif command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y dnf-plugins-core
  sudo dnf config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
  sudo dnf install -y terraform
else
  echo "no brew/apt/dnf found -- see https://developer.hashicorp.com/terraform/install" >&2
  exit 1
fi
