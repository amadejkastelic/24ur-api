{pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-unstable") {}}:
pkgs.mkShell {
  packages = with pkgs; [
    python312
    python312Packages.pip
    pipenv
    ffmpeg
    curl
    jq
  ];
}
