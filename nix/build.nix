{
  pythonPkgs,
  pythonProject,
}:

pythonPkgs.buildPythonPackage {
  pname = pythonProject.project.name;
  version = pythonProject.project.version;
  pyproject = true;

  src = ../.;

  build-system = [ pythonPkgs.hatchling ];

  dependencies = [
    pythonPkgs.aiohttp
    pythonPkgs.yt-dlp
  ];

  # We need to also build the source distribution if building dist
  preInstall = ''
    hatchling build -t sdist
  '';

  postInstall = ''
    cp dist/*.tar.gz $out
  '';

  pythonImportsCheck = [ "api_24ur" ];
}
