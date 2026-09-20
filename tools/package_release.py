#!/usr/bin/env python3
from pathlib import Path
import argparse, subprocess, tempfile, sys, hashlib, tomllib

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'


def run(*args, cwd=ROOT):
    return subprocess.run(args,cwd=cwd,check=True,text=True,capture_output=True)


def project():
    return tomllib.loads((ROOT/'pyproject.toml').read_text())['project']

def version():
    return project()['version']

def slug():
    return project()['name']


def ensure_clean():
    if run('git','status','--porcelain').stdout.strip():
        raise SystemExit('refusing distribution from dirty working tree; commit or stash first')


def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()


def build():
    ensure_clean(); DIST.mkdir(exist_ok=True)
    name=slug(); ver=version(); zipf=DIST/f'{name}-v{ver}.zip'; bundle=DIST/f'{name}-v{ver}.bundle'; sums=DIST/'SHA256SUMS.txt'; release=DIST/'RELEASE.txt'
    for p in (zipf,bundle,sums,release):
        if p.exists(): p.unlink()
    subprocess.run(['git','archive','--format=zip',f'--prefix={name}/','-o',str(zipf),'HEAD'],cwd=ROOT,check=True)
    # Include symbolic HEAD and main so ordinary clones preserve the intended default branch history.
    commit=run('git','rev-parse','HEAD').stdout.strip()
    refs=['HEAD','main']
    tag=f'v{ver}'
    tag_check=subprocess.run(['git','rev-parse','-q','--verify',f'{tag}^{{commit}}'],cwd=ROOT,text=True,capture_output=True)
    if tag_check.returncode==0 and tag_check.stdout.strip()==commit:
        refs.append(tag)
    subprocess.run(['git','bundle','create',str(bundle),*refs],cwd=ROOT,check=True)
    release.write_text(f'HowlFutureWorks / {name} v{version()}\ncommit {commit}\nbranch main\n')
    sums.write_text(f'{sha256(zipf)}  {zipf.name}\n{sha256(bundle)}  {bundle.name}\n{sha256(release)}  {release.name}\n')
    for p in (zipf,bundle,release,sums): print(p)


def verify_checksums(sums):
    for line in sums.read_text().splitlines():
        expected,name=line.split(None,1); name=name.strip()
        p=DIST/name
        if not p.exists(): raise SystemExit(f'missing distribution file {name}')
        actual=sha256(p)
        if actual!=expected: raise SystemExit(f'checksum mismatch for {name}: {actual} != {expected}')


def verify():
    name=slug(); ver=version(); zipf=DIST/f'{name}-v{ver}.zip'; bundle=DIST/f'{name}-v{ver}.bundle'; sums=DIST/'SHA256SUMS.txt'; release=DIST/'RELEASE.txt'
    if not all(p.exists() for p in (zipf,bundle,sums,release)): raise SystemExit('run dist first')
    verify_checksums(sums)
    subprocess.run(['unzip','-t',str(zipf)],check=True,stdout=subprocess.DEVNULL)
    subprocess.run(['git','bundle','verify',str(bundle)],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
    heads=run('git','bundle','list-heads',str(bundle)).stdout
    if 'refs/heads/main' not in heads or ' HEAD' not in heads:
        raise SystemExit('bundle must advertise both HEAD and refs/heads/main')
    tag=f'v{version()}'
    tag_check=subprocess.run(['git','rev-parse','-q','--verify',f'{tag}^{{commit}}'],cwd=ROOT,text=True,capture_output=True)
    if tag_check.returncode==0 and tag_check.stdout.strip()==run('git','rev-parse','HEAD').stdout.strip() and f'refs/tags/{tag}' not in heads:
        raise SystemExit(f'bundle must include release tag {tag} when it points at HEAD')
    expected=run('git','rev-parse','HEAD').stdout.strip()
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); z=td/'zip'; c=td/'clone'; z.mkdir()
        subprocess.run(['unzip','-q',str(zipf),'-d',str(z)],check=True)
        subprocess.run(['git','clone','-q','-b','main',str(bundle),str(c)],check=True)
        if run('git','rev-parse','HEAD',cwd=c).stdout.strip()!=expected:
            raise SystemExit('bundle clone commit does not match release commit')
        # Compare pristine archive contents to the bundle clone's tracked tree byte-for-byte
        # before validation/tests create caches or other untracked files.
        tracked=run('git','ls-files',cwd=c).stdout.splitlines()
        zip_root=z/name
        zip_files=sorted(str(x.relative_to(zip_root)) for x in zip_root.rglob('*') if x.is_file())
        if sorted(tracked)!=zip_files:
            raise SystemExit('ZIP and bundle tracked file lists differ')
        for rel in tracked:
            if (zip_root/rel).read_bytes()!=(c/rel).read_bytes():
                raise SystemExit(f'ZIP and bundle content differ: {rel}')
        for tree in (zip_root,c):
            subprocess.run([sys.executable,'tools/orgctl.py','validate'],cwd=tree,check=True)
            subprocess.run([sys.executable,'-m','pytest','-q'],cwd=tree,check=True)
    print('distribution verification passed; ZIP and bundle trees are identical')


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('command',choices=['build','verify']); a=ap.parse_args()
    build() if a.command=='build' else verify()
if __name__=='__main__': main()
