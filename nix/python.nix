{ python }:

let
  venv = python.withPackages (
    ps: with ps; [
      aiohttp
      yt-dlp
      ruff
    ]
  );
in
{
  inherit venv;
}
