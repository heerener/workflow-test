#!/usr/bin/env python

import os

from git import Repo

keywords = ['nopackage', 'deploy']

repo = Repo('.')
commit_packages = []

for commit in repo.iter_commits():
    commit_packages.append((commit.hexsha, commit.message.split(':')[0]))
# package = repo.head.commit.message.split(':')[0]

existing_packages = []
for spack_repo in ['./var/spack/repos/builder.test',
                   './var/spack/repos/builtin',
                   './var/spack/repos/builtin.mock',
                   './var/spack/repos/tutorial',
                   './bluebrain/repo-bluebrain',
                   './bluebrain/repo-patches']:
    existing_packages.extend(os.walk(f'{spack_repo}/packages'))

faulty_commits = []
for commit_info in commit_packages:
    sha, package = commit_info
    if package.strip() not in existing_packages and package not in keywords:
        msg = f'Commit {sha} message "{repo.head.commit.message}" does not follow the required template.\n'
        msg += f'"{package}" is not a known package or one of {keywords}\n'
        msg += 'Please reformat your commit message to start with either a package name, '
        msg += f'or one of {keywords} followed by a :'
        faulty_commits.append(msg)

raise ValueError('\n'.join(faulty_commits))
