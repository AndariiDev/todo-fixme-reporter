{
  description = "A simple TODO/FIXME reporter for code projects";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, description ? "A simple TODO/FIXME reporter for code projects" }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (system: f system);

      todoReporterPackageFun = { pkgs, description }: pkgs.stdenv.mkDerivation {
        pname = "todo-fixme-reporter";
        version = "0.1.0";
        src = ./.;
        buildInputs = [ pkgs.python3 ];
        installPhase = ''
          mkdir -p $out/bin
          cp $src/reporter.py $out/bin/todo-reporter-cli
          chmod +x $out/bin/todo-reporter-cli
        '';
        meta = with pkgs.lib; {
          description = description;
          homepage = "https://github.com/AndariiDev/todo-fixme-reporter";
          license = licenses.mit;
        };
      };
    in
    {
      apps = forAllSystems (system:
        let pkgs = import nixpkgs { inherit system; }; in
        {
          default = {
            type = "app";
            program = "${(todoReporterPackageFun { pkgs = pkgs; description = self.description; })}/bin/todo-reporter-cli";
          };
        }
      );

      packages = forAllSystems (system:
        let pkgs = import nixpkgs { inherit system; }; in
        {
          default = todoReporterPackageFun { pkgs = pkgs; description = description; };
        }
      );

      devShells = forAllSystems (system:
        let pkgs = import nixpkgs { inherit system; }; in
        {
          default = pkgs.mkShell {
            packages = [ pkgs.python3 ];
          };
        }
      );
    };
}
