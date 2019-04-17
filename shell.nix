with import <nixpkgs> {};

mkShell {
  buildInputs = [
    python37
    google-cloud-sdk
  ];
  DJANGO_SETTINGS_MODULE = "travelfootprint.settings";
  shellHook = ''
    [[ -d .env ]] || make init
    source .venv/bin/activate
  '';
}
