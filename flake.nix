{
  description = "The Hive - The secretly open NixOS-Society";
  inputs.std.url = "github:divnix/std";
  inputs.std.inputs.nixpkgs.follows = "nixpkgs";
  inputs.std.inputs.mdbook-kroki-preprocessor.follows = "std/blank";
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";

  outputs = {
    std,
    self,
    ...
  } @ inputs:
    std.growOn {
      inherit inputs;
      cellsFrom = ./comb;
      # debug = ["cells" "x86_64-linux"];
      cellBlocks = with std.blockTypes; [
        # devshells can be entered
        (devshells "devshells")
      ];
      nixpkgsConfig = {
        allowUnfree = true;
      };
    }
    # soil
    {
      devShells = std.harvest self ["_QUEEN" "devshells"];
    };
}
