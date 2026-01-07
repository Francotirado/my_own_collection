#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_module

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
  path:
    description:
      - Path to the file to create or update.
    required: true
    type: str
  content:
    description:
      - Content to write into the file.
    required: true
    type: str

author:
    - Roman Perevozchikov (@Francotirado)
'''

EXAMPLES = r'''
- name: Test with a message
  my_module:
    path: ./hello.txt
    name: "Hello World!"
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
path:
  description: Path of the file that was created/updated.
  type: str
  returned: always
  sample: "./hello.txt"
'''

import os
from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        path=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    changed = False
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            current_content = f.read()
        if current_content != content:
            changed = True
    else:
        changed = True

    if module.check_mode:
        module.exit_json(changed=changed, path=path)

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    result['changed'] = changed
    result['path'] = path
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
