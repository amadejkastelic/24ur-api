{
  description = "API Client for 24ur.com";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs =
    {
      nixpkgs,
      flake-parts,
      ...
    }@inputs:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "aarch64-linux"
        "aarch64-darwin"
        "x86_64-linux"
        "x86_64-darwin"
      ];

      perSystem =
        {
          pkgs,
          system,
          ...
        }:
        let
          python = pkgs.python313;

          pythonConfig = import ./nix/python.nix {
            inherit
              python
              ;
          };

          inherit (pythonConfig) venv;
        in
        {
          formatter = pkgs.nixfmt-tree;

          checks = import ./nix/checks.nix {
            inherit pkgs;
            venv = venv;
            nixfmt-tree = pkgs.nixfmt-tree;
          };

          packages = {
            default = import ./nix/build.nix {
              pythonProject = pkgs.lib.importTOML ./pyproject.toml;
              pythonPkgs = pkgs.python313Packages;
            };
          };

          devShells.default = import ./nix/shell.nix {
            inherit pkgs;
            venv = venv;
          };
        };
    };
}
