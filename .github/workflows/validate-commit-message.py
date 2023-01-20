#!/usr/bin/env python

import os

from git import Repo

keywords = ['nopackage', 'deploy']

repo = Repo('.')
package = repo.head.commit.message.split(':')[0]
existing_packages = []

for spack_repo in ['./var/spack/repos/builder.test',
                   './var/spack/repos/builtin',
                   './var/spack/repos/builtin.mock',
                   './var/spack/repos/tutorial',
                   './bluebrain/repo-bluebrain',
                   './bluebrain/repo-patches']:
    existing_packages.extend(os.walk(f'{spack_repo}/packages'))

if package not in existing_packages and package not in keywords:
    msg = f'Commit message "{repo.head.commit.message}" does not follow the required template\n'
    msg += f'{package} is not a known package or one of {keywords}\n'
    msg += 'Please reformat your commit message'
    raise ValueError(msg)
