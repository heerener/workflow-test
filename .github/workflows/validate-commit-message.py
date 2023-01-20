#!/usr/bin/env python

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
    existing_packages.extend(os.walk(f'{spack_repo}/packages'))

print(existing_packages)
faulty_commits = []
for commit in repo.iter_commits():
    if len(commit.parents) > 1:
        print('Not going beyond a merge commit')
        break

    package = commit.message.split(':')[0]
    if package.strip() not in existing_packages and package not in keywords:
        msg = f'Commit {commit.hexsha} message "{commit.message.rstrip()}" does not follow the required template.\n'
        msg += f'"{package}" is not a known package or one of {keywords}\n'
        msg += 'Please reformat your commit message to start with either a package name, '
        msg += f'or one of {keywords} followed by a :\n'
        msg += 30 * '='
        faulty_commits.append(msg)

if faulty_commits:
    raise ValueError('\n'.join(faulty_commits))
