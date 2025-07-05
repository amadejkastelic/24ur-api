{
  pkgs,
  venv,
  nixfmt-tree,
}:
let
  src = ./..;

  runCheck =
    name: command:
    pkgs.runCommand name
      {
        nativeBuildInputs = [
          venv
          nixfmt-tree
        ];
        src = src;
      }
      ''
        cd ${src}
        export PATH=${venv}/bin:$PATH
        export TREEFMT_TREE_ROOT=${src}
        export RUFF_NO_CACHE=true
        ${command}
        touch $out
      '';
in
{
  ruff = runCheck "ruff" "ruff check api_24ur";
  nixfmt = runCheck "nixfmt" "treefmt --ci";
}
