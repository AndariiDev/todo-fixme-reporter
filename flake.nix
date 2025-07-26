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
    forAllSystems (system: # We apply the function for all systems at this top-level
      let
        pkgs = import nixpkgs { inherit system; };

        # --- Define the actual PACKAGE (derivation) that holds your script ---
        # This creates a result in /nix/store/.../todo-fixme-reporter/bin/todo-reporter-cli
        todoReporterPackage = pkgs.stdenv.mkDerivation {
          pname = "todo-fixme-reporter";
          version = "0.1.0"; # Version of your package

          src = ./.; # The source of your entire repo (where reporter.py is)

          # Build dependencies: We need python3 during the installation phase
          buildInputs = [ pkgs.python3 ];

          # This defines what happens during the build process to put the script into the $out path
          installPhase = ''
            mkdir -p $out/bin # Create the bin directory in the output
            cp $src/reporter.py $out/bin/todo-reporter-cli # Copy your script into it
            chmod +x $out/bin/todo-reporter-cli # Make it executable
          '';

          # Optional: Metadata for the package, useful for nixpkgs contribution later
          meta = with pkgs.lib; {
            description = self.description; # Uses the description from the flake
            homepage = "https://github.com/AndariiDev/todo-fixme-reporter"; # Link to your repo
            license = licenses.mit;
            # maintainers = [ maintainers.your_github_handle_here ]; # Uncomment and fill if you add yourself to pkgs.maintainers
          };
        };

      in
      {
        # --- Define the 'apps' output, which just points to the executable inside our package ---
        # This makes 'nix run .' work
        apps.default = {
          type = "app";
          program = "${todoReporterPackage}/bin/todo-reporter-cli"; # Points to the executable inside the package
        };

        # --- Define the 'packages' output, so it can be built and installed separately ---
        # This makes 'nix build .' and 'nix profile install .' work
        packages.default = todoReporterPackage;

        # --- Define the 'devShells' output for development environment ---
        # This makes 'nix develop' work
        devShells.default = pkgs.mkShell {
          packages = [ pkgs.python3 ]; # Ensures python3 is in your shell
          # You can add other tools for development here, e.g., pkgs.helix, pkgs.git
        };
      }
    );
}
