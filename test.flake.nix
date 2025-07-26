{
  description = "A simple TODO/FIXME reporter for code projects";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (system: f system);
    in
    {
      apps = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        {
          default = {
            type = "app";
            program = "${pkgs.writeShellScriptBin "todo-reporter-app" ''
              export PATH=${pkgs.python3}/bin:$PATH
              exec ${pkgs.python3}/bin/python ${./reporter.py} "$@"
            ''}";
         };
        }
      );

      devShells = forAllSystems (system:
        let pkgs = import nixpkgs { inherit system; }; in {
          default = pkgs.mkShell{
            packages = [ pkgs.python3 ];
          };
        }
      );
    };
}
