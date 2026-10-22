#!/usr/bin/env python3
"""Capture actual project verification output and exit status without caching."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

def git(repo, *args):
    try:
        result = subprocess.run(['git', '-C', str(repo), *args],
                                capture_output=True, check=False)
        return result.stdout if result.returncode == 0 else None
    except FileNotFoundError:
        return None


def snapshot(repo, evidence):
    """Hash working contents, not the index. Never follow symlinks to secrets."""
    names = git(repo, 'ls-files', '-z', '--cached', '--others', '--exclude-standard')
    if names is None:
        paths = [p for p in repo.rglob('*') if '.git' not in p.relative_to(repo).parts
                 and (p.is_symlink() or not p.is_dir())]
        scope = 'Directory files, no Git ignore rules available; evidence excluded.'
    else:
        paths = [repo / os.fsdecode(name) for name in set(names.split(b'\0')) if name]
        scope = 'Git tracked and untracked non-ignored paths under repo; evidence excluded.'
    files = []
    for path in sorted(paths):
        # Keep the path lexical so an external symlink is described, not followed.
        if path.is_relative_to(evidence):
            continue
        entry = {'path': path.relative_to(repo).as_posix()}
        parts = path.relative_to(repo).parts
        for length in range(1, len(parts)):
            parent = repo.joinpath(*parts[:length])
            if parent.is_symlink():
                entry.update(kind='unfingerprinted-symlink-parent',
                             boundary=parent.relative_to(repo).as_posix())
                break
        if 'boundary' in entry:
            files.append(entry)
            continue
        try:
            info = path.lstat()
        except (FileNotFoundError, NotADirectoryError):
            entry['kind'] = 'missing'
        else:
            entry['mode'] = oct(stat.S_IMODE(info.st_mode))
            if stat.S_ISLNK(info.st_mode):
                entry.update(kind='symlink', sha256=hashlib.sha256(
                    os.fsencode(os.readlink(path))).hexdigest())
            elif stat.S_ISREG(info.st_mode):
                digest = hashlib.sha256()
                with path.open('rb') as source:
                    for chunk in iter(lambda: source.read(1024 * 1024), b''):
                        digest.update(chunk)
                entry.update(kind='file', sha256=digest.hexdigest())
            else:
                entry['kind'] = 'unfingerprinted-directory-or-special-file'
        files.append(entry)
    revision = git(repo, 'rev-parse', 'HEAD')
    digest = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    return {'revision': revision.decode().strip() if revision else None,
            'files': files, 'digest': digest, 'scope': scope}


def setup_context(path):
    if path is None:
        return None
    value = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(value, dict):
        raise ValueError('Setup context must be a JSON object with nonsecret descriptions')
    return value


def verify(repo, evidence, command, context=None):
    repo, evidence = Path(repo).resolve(), Path(evidence).resolve()
    if not repo.is_dir() or not command:
        raise ValueError('Existing repository and verification command required')
    if repo.is_relative_to(evidence):
        raise ValueError('Evidence cannot contain the repository being tested')
    evidence.mkdir(parents=True, exist_ok=True)
    if any((evidence / name).exists() for name in ('output.log', 'result.json')):
        raise ValueError('Evidence already exists; choose a new directory')
    # Evidence destinations must be new; never erase a prior run.
    with (evidence / 'output.log').open('x', encoding='utf-8') as output:
        before, setup_before = snapshot(repo, evidence), setup_context(context)
        started = datetime.now(timezone.utc).isoformat()
        launch_error = None
        try:
            status = subprocess.run(command, cwd=repo, stdout=output,
                                    stderr=subprocess.STDOUT, check=False).returncode
        except OSError as exc:
            status, launch_error = 127, str(exc)
            output.write(launch_error + '\n')
        finished = datetime.now(timezone.utc).isoformat()
        capture_error = None
        try:
            after, setup_after = snapshot(repo, evidence), setup_context(context)
        except (ValueError, OSError) as exc:
            after, setup_after, capture_error = None, None, str(exc)
    record = {'command': command, 'repo': str(repo), 'exit_code': status,
              'revision': before['revision'], 'time': started, 'finished': finished,
              'before': before, 'after': after,
              'setup_before': setup_before, 'setup_after': setup_after,
              'changed_during_run': before != after or setup_before != setup_after,
              'limits': 'No automatic reuse. Snapshots are observations, not a lock. '
                        'Git-ignored files, symlink targets, submodule contents and external '
                        'services/data are not identified. Setup is caller-described, not '
                        'verified. No environment variables or file contents are copied. '
                        'Command output and arguments may contain secrets; redact at source.'}
    if launch_error:
        record['launch_error'] = launch_error
    if capture_error:
        record['capture_error'] = capture_error
    with (evidence / 'result.json').open('x', encoding='utf-8') as dest:
        json.dump(record, dest, indent=2)
    print(json.dumps({'exit_code': status, 'revision': record['revision'],
                      'changed_during_run': record['changed_during_run'],
                      'capture_error': capture_error,
                      'result': str(evidence / 'result.json')}))
    return status or (1 if capture_error else 0)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True)
    parser.add_argument('--evidence', required=True)
    parser.add_argument('--context', help='JSON object of nonsecret setup descriptions')
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    try:
        return verify(args.repo, args.evidence, command, args.context)
    except (ValueError, OSError) as exc:
        parser.exit(1, str(exc) + '\n')

if __name__ == '__main__':
    sys.exit(main())
