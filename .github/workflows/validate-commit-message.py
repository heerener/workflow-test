#!/usr/bin/env python

# requires: gitpython

import os

from git import Repo

keywords = ['nopackage', 'deploy']

repo = Repo('.')

existing_packages = []
for spack_repo in ['./var/spack/repos/builder.test',
                   './var/spack/repos/builtin',
                   './var/spack/repos/builtin.mock',
                   './var/spack/repos/tutorial',
                   './bluebrain/repo-bluebrain',
                   './bluebrain/repo-patches']:
    try:
        existing_packages.extend(next(os.walk(f'{spack_repo}/packages'))[1])
    except StopIteration:
        print(f'No packages under {spack_repo}')
        pass

faulty_commits = []
for commit in repo.iter_commits():
    print(f'Commit: {commit.message} (parents: {commit.parents})')
    if len(commit.parents) > 1:
        print('Not going beyond a merge commit')
        break

    package = commit.message.splitlines()[0].split(':')[0]
    if package.strip() not in existing_packages and package not in keywords:
        quoted_commit_message = '\n'.join([f'> {line} for line in commit.message.splitlines()'])
        msg = f'### {commit.hexsha}\n'
        msg += f'{quoted_commit_message}\n\n'
        msg += f'Commit message does not follow the required template.\n'
        msg += f'"{package}" is not a known package or one of {keywords}\n'
        msg += 'Please amend your commit message to start with either a package name, '
        msg += f'or one of {keywords} followed by a ":"\n'
        faulty_commits.append(msg)

if faulty_commits:
    with open('faulty_commits.txt', 'w') as fp:
        fp.write('\n'.join(faulty_commits))
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fp:
        fp.write("faulty-commits=true")
