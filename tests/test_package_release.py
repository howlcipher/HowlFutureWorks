import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git(repo, *args, check=True):
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=check,
        capture_output=True,
        text=True,
    )


def sha(repo, ref):
    r = git(repo, "rev-parse", "--verify", ref)
    return r.stdout.strip()


def has_ref(repo, ref):
    return git(repo, "rev-parse", "-q", "--verify", ref, check=False).returncode == 0


def init_packaging_repo(tmp_path, *, extra_files=None):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "tools").mkdir()
    shutil.copy(ROOT / "tools" / "package_release.py", repo / "tools" / "package_release.py")
    (repo / "pyproject.toml").write_text(
        '[project]\nname = "howl-future-works"\nversion = "0.4.1"\n'
    )
    (repo / "README.md").write_text("packaging fixture\n")
    for rel, text in (extra_files or {}).items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    git(repo, "init", "-b", "main")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "HowlFutureWorks Tests")
    git(repo, "config", "commit.gpgsign", "false")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "initial")
    return repo


def build_dist(repo):
    return subprocess.run(
        [sys.executable, str(repo / "tools" / "package_release.py"), "build"],
        cwd=repo,
        capture_output=True,
        text=True,
    )


def bundle_path(repo):
    matches = list((repo / "dist").glob("*.bundle"))
    assert len(matches) == 1, matches
    return matches[0]


def bundle_heads(repo):
    r = subprocess.run(
        ["git", "bundle", "list-heads", str(bundle_path(repo))],
        check=True,
        capture_output=True,
        text=True,
    )
    return r.stdout


def clone_bundle_main(repo, dest):
    subprocess.run(
        ["git", "clone", "-q", "-b", "main", str(bundle_path(repo)), str(dest)],
        check=True,
        capture_output=True,
        text=True,
    )


def test_package_release_with_local_main(tmp_path):
    repo = init_packaging_repo(tmp_path)
    head = sha(repo, "HEAD")
    main = sha(repo, "refs/heads/main")
    assert head == main
    assert git(repo, "symbolic-ref", "-q", "HEAD").stdout.strip() == "refs/heads/main"

    result = build_dist(repo)
    assert result.returncode == 0, result.stderr

    assert sha(repo, "HEAD") == head
    assert sha(repo, "refs/heads/main") == main
    assert git(repo, "symbolic-ref", "-q", "HEAD").stdout.strip() == "refs/heads/main"

    heads = bundle_heads(repo)
    assert "refs/heads/main" in heads
    assert " HEAD" in heads
    assert head in heads

    clone = tmp_path / "clone"
    clone_bundle_main(repo, clone)
    assert sha(clone, "HEAD") == head
    assert sha(clone, "refs/heads/main") == head


def test_package_release_detached_without_local_main(tmp_path):
    repo = init_packaging_repo(tmp_path)
    head = sha(repo, "HEAD")
    git(repo, "checkout", "--detach", "HEAD")
    git(repo, "branch", "-D", "main")
    assert not has_ref(repo, "refs/heads/main")
    assert git(repo, "symbolic-ref", "-q", "HEAD", check=False).returncode != 0

    result = build_dist(repo)
    assert result.returncode == 0, result.stderr

    assert sha(repo, "HEAD") == head
    assert not has_ref(repo, "refs/heads/main")
    assert git(repo, "symbolic-ref", "-q", "HEAD", check=False).returncode != 0

    heads = bundle_heads(repo)
    assert "refs/heads/main" in heads
    assert " HEAD" in heads
    assert head in heads

    clone = tmp_path / "clone"
    clone_bundle_main(repo, clone)
    assert sha(clone, "HEAD") == head
    assert sha(clone, "refs/heads/main") == head


def test_package_release_restores_divergent_main(tmp_path):
    repo = init_packaging_repo(tmp_path)
    original_main = sha(repo, "refs/heads/main")
    git(repo, "checkout", "--detach", "HEAD")
    (repo / "README.md").write_text("divergent packaged HEAD\n")
    git(repo, "add", "README.md")
    git(repo, "commit", "-m", "packaged head")
    packaged = sha(repo, "HEAD")
    assert packaged != original_main
    assert sha(repo, "refs/heads/main") == original_main

    result = build_dist(repo)
    assert result.returncode == 0, result.stderr

    assert sha(repo, "HEAD") == packaged
    assert sha(repo, "refs/heads/main") == original_main
    assert git(repo, "symbolic-ref", "-q", "HEAD", check=False).returncode != 0

    heads = bundle_heads(repo)
    assert "refs/heads/main" in heads
    advertised = {
        line.split()[1]: line.split()[0]
        for line in heads.splitlines()
        if line.strip()
    }
    assert advertised["refs/heads/main"] == packaged
    assert advertised["HEAD"] == packaged

    clone = tmp_path / "clone"
    clone_bundle_main(repo, clone)
    assert sha(clone, "HEAD") == packaged
    assert sha(clone, "refs/heads/main") == packaged
