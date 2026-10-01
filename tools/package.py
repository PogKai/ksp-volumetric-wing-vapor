"""Build the release DLL and package Volumetric Wing Vapor as a KSP mod zip.

    python tools/package.py                  package the committed state (the normal case)
    python tools/package.py --allow-dirty    package the working tree, for a release candidate
    python tools/package.py --update-plugin  also copy the built DLL over
                                             Plugins/VolumetricWingVapor.dll, which the repository tracks

Writes dist/VolumetricWingVapor_<version>.zip in the layout KSP mods are installed in:

    GameData/VolumetricWingVapor/Plugins/VolumetricWingVapor.dll
    GameData/VolumetricWingVapor/Source/*.cs
    GameData/VolumetricWingVapor/README.md, CHANGELOG.md, license.md
    GameData/VolumetricWingVapor/docs/*.md

then reads the zip back and checks that the DLL inside is the one just built. Refuses to run when

  * the version in Source/AssemblyInfo.cs and in the top heading of CHANGELOG.md disagree, or
    the KSPAssembly attribute does not carry that version's major and minor,
  * tracked files have uncommitted changes (unless --allow-dirty), so a release is always a commit,
  * the DLL was compiled against a test build of Wingtip Vortex (an assembly not named
    WingtipVortex), which players do not have.

The paths to KSP and to WingtipVortex.dll come from local.props; see README.md.
"""
import hashlib
import os
import re
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = "VolumetricWingVapor"
CSPROJ = os.path.join(ROOT, NAME + ".csproj")
DIST = os.path.join(ROOT, "dist")
BUILD = os.path.join(DIST, "build")


def read(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.read()


def run(*cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def main():
    allow_dirty = "--allow-dirty" in sys.argv
    update_plugin = "--update-plugin" in sys.argv

    assembly_info = read(os.path.join(ROOT, "Source", "AssemblyInfo.cs"))
    assembly = re.search(r'AssemblyVersion\("(\d+\.\d+\.\d+)\.0"\)', assembly_info)
    heading = re.search(r"^## (\S+)", read(os.path.join(ROOT, "CHANGELOG.md")), re.M)
    found = [m and m.group(1) for m in (assembly, heading)]
    if not (found[0] and found[0] == found[1]):
        sys.exit("versions must agree and be numeric: AssemblyInfo %s, top of CHANGELOG %s" % tuple(found))
    version = found[0]
    ksp = re.search(r'KSPAssembly\("%s", (\d+), (\d+)\)' % NAME, assembly_info)
    if not ksp or version.split(".")[:2] != list(ksp.groups()):
        sys.exit("the KSPAssembly attribute in AssemblyInfo.cs must carry %s's major and minor" % version)

    dirty = run("git", "status", "--porcelain", "--untracked-files=no").stdout.strip()
    if dirty and not allow_dirty:
        sys.exit("uncommitted changes to tracked files, so this would not be a release of a commit:\n" + dirty +
                 "\ncommit them, or use --allow-dirty for a release candidate")

    print("building %s %s (Release)" % (NAME, version))
    os.makedirs(BUILD, exist_ok=True)
    result = run("dotnet", "build", CSPROJ, "-c", "Release", "-nologo", "-v", "q",
                 "-p:OutputPath=" + BUILD + os.sep)
    if result.returncode != 0:
        sys.exit(result.stdout + result.stderr)
    dll = os.path.join(BUILD, NAME + ".dll")
    with open(dll, "rb") as f:
        built = f.read()
    if b"WingtipVortex_" in built or b"WingtipVortex" not in built:
        sys.exit("the DLL must be compiled against the release WingtipVortex.dll: check VortexDll in local.props")

    root = "GameData/" + NAME + "/"
    files = {root + "Plugins/" + NAME + ".dll": dll}
    for doc in ("README.md", "CHANGELOG.md", "license.md"):
        files[root + doc] = os.path.join(ROOT, doc)
    docs = os.path.join(ROOT, "docs")
    for name in sorted(os.listdir(docs)):
        if name.endswith(".md"):
            files[root + "docs/" + name] = os.path.join(docs, name)
    source = os.path.join(ROOT, "Source")
    for name in sorted(os.listdir(source)):
        if name.endswith(".cs"):
            files[root + "Source/" + name] = os.path.join(source, name)

    out = os.path.join(DIST, "%s_%s.zip" % (NAME, version))
    if os.path.exists(out):
        os.remove(out)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for arc, path in files.items():
            info = zipfile.ZipInfo(arc, date_time=(2026, 1, 1, 0, 0, 0))   # same bytes for the same inputs
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(path, "rb") as f:
                z.writestr(info, f.read())

    with zipfile.ZipFile(out) as z:
        names = z.namelist()
        bad = [n for n in names if re.search(r"(^|/)(bin|obj|dist|tools)/|\.pdb$|\.props$|\\", n)]
        if bad or any(not n.startswith(root) for n in names):
            sys.exit("unexpected files in the package: " + ", ".join(bad or names))
        if z.read(root + "Plugins/" + NAME + ".dll") != built:
            sys.exit("the DLL in the zip is not the one just built")
        if ("## " + version) not in z.read(root + "CHANGELOG.md").decode("utf-8"):
            sys.exit("changelog does not mention " + version)

    if update_plugin:
        with open(os.path.join(ROOT, "Plugins", NAME + ".dll"), "wb") as dst:
            dst.write(built)
        print("updated Plugins/%s.dll" % NAME)

    print("wrote %s (%s bytes)" % (os.path.relpath(out, ROOT), format(os.path.getsize(out), ",")))
    print("sha256 " + hashlib.sha256(open(out, "rb").read()).hexdigest())
    for n in names:
        print("  " + n)


if __name__ == "__main__":
    main()
