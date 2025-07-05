{
  pkgs,
  venv,
}:
pkgs.mkShell {
  packages = [
    venv
    pkgs.httptoolkit
    pkgs.nixfmt-tree
    pkgs.twine
  ];

  # Workaround: make vscode's python extension read the .venv
  shellHook = ''
    venv="$(cd $(dirname $(which python)); cd ..; pwd)"
    ln -Tsf "$venv" .venv
  '';
}
