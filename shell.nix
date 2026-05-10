{ pkgs ? import <nixpkgs> {} }:

let
  python = pkgs.python3.withPackages (ps: with ps; [
    numpy
    scipy
    soundfile
    matplotlib
    pyqt5
  ]);
in
pkgs.mkShell {
  packages = [
    python
    pkgs.qt5.qtbase
  ];

  shellHook = ''
    export QT_QPA_PLATFORM_PLUGIN_PATH=${pkgs.qt5.qtbase}/lib/qt-${pkgs.qt5.qtbase.version}/plugins/platforms
    echo "afra dev shell ready. Run: python main.py <audio-file>"
  '';
}
