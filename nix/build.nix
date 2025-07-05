{
  pythonPkgs,
  pythonProject,
}:

pythonPkgs.buildPythonPackage {
  pname = pythonProject.project.name;
  version = pythonProject.project.version;
  pyproject = true;

  src = ../.;

  build-system = [ pythonPkgs.setuptools ];

  pythonRelaxDeps = [ "beautifulsoup4" ];

  dependencies = [
    pythonPkgs.aiohttp
    pythonPkgs.yt-dlp
  ];

  pythonImportsCheck = [ "api_24ur" ];

  postInstall = ''
    cp dist/*.whl $out/
  '';
}
