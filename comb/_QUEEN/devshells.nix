let
  l = nixpkgs.lib // builtins;

  inherit (inputs) nixpkgs std;
  inherit (std.lib) dev;

  withCategory = category: attrset: attrset // {inherit category;};

  python = "python310";
in
  l.mapAttrs (_: dev.mkShell) {
    default = {...}: {
      name = "Apis Mellifera";
      nixago = with std.presets.nixago; [
        treefmt
        lefthook
        editorconfig
        (conform {configData = {inherit (inputs) cells;};})
      ];
      imports = [];
      packages = with nixpkgs; [
        poetry
        (python310.withPackages
          (ps:
            with ps; [
              # pkg
              typer
              black
              isort
              pytest
              pydantic
              jupyter
              #loguru
              pandas
              requests
              # DB
              psycopg2
              fastapi
              uvicorn
              websockets
            ])) # <--- change here
      ];
      commands = [
        (withCategory "hexagon" {
          name = "start-api";
          help = "Start the fastapi server at port 8000";
          command = ''
            cp $PRJ_ROOT/src/unbabel/calc.py $PRJ_ROOT/src/server
            cd $PRJ_ROOT/src/server
            uvicorn api:app --reload &
          '';
        })
        (withCategory "hexagon" {
          name = "stop-api";
          help = "Stop the fastapi server at port 8000";
          command = ''
            rm $PRJ_ROOT/src/server/calc.py
            killall .uvicorn-wrapper
          '';
        })
        (withCategory "hexagon" {
          name = "start-psql";
          help = "Start the psql database at port 5432";
          command = ''
            dockerd &
            docker-compose up --detach database
          '';
        })
        (withCategory "hexagon" {
          name = "stop-psql";
          help = "Start the psql database at port 5432";
          command = ''
            docker image rm postgres:latest -f
            killall dockerd
          '';
        })
        (withCategory "hexagon" {
          name = "kill-service";
          help = "Start the psql database at port 5432";
          command = ''
            docker image rm postgres:latest -f
            killall dockerd
          '';
        })
        (withCategory "hexagon" {
          name = "start-service";
          help = "Launch the whole service";
          command = ''
            dockerd &
            docker-compose up --detach
          '';
        })
      ];
    };
  }
