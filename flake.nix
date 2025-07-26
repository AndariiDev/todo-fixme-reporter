{
  description = "A simple TODO/FIXME reporter for code projects";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: # This is the function for the entire outputs attribute set
    let
      # --- Define shared helpers and variables here (at the top of 'outputs' let-in) ---
      supportedSystems = [ "x86_64-linux" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (system: f system);

      # Define the 'todoReporterPackage' ONCE here if it's used by multiple outputs.
      # This avoids redefining it inside each 'forAllSystems' block.
      # It takes 'pkgs' as an argument so it can be defined once and applied to each system's pkgs later.
      todoReporterPackageFun = pkgs: pkgs.stdenv.mkDerivation {
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
          description = self.description;
          homepage = "https://github.com/AndariiDev/todo-fixme-reporter";
          license = licenses.mit;
        };
      };
    in
    { # <--- This is the main outputs attribute set (it's NOT wrapped by forAllSystems here)

      # --- 1. Define the 'apps' output (for 'nix run .') ---
      apps = forAllSystems (system: # Apply forAllSystems only to the 'apps' block
        let pkgs = import nixpkgs { inherit system; }; in
        {
          default = {
            type = "app";
            program = "${(todoReporterPackageFun pkgs)}/bin/todo-reporter-cli"; # Call the package function with pkgs
          };
        }
      );

      # --- 2. Define the 'packages' output (for 'nix build .' and 'nix profile install .') ---
      packages = forAllSystems (system: # Apply forAllSystems only to the 'packages' block
        let pkgs = import nixpkgs { inherit system; }; in
        {
          default = todoReporterPackageFun pkgs; # Call the package function with pkgs
        }
      );

      # --- 3. Define the 'devShells' output (for 'nix develop') ---
      devShells = forAllSystems (system: # Apply forAllSystems only to the 'devShells' block
        let pkgs = import nixpkgs { inherit system; }; in
        {
          default = pkgs.mkShell {
            packages = [ pkgs.python3 ];
          };
        }
      );

    }; # <--- End of the main outputs attribute set
}
