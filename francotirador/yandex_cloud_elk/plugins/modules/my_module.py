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
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        path=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    path = module.params['path']
    content = module.params['content']

    # Check if file exists and content matches
    file_exists = os.path.exists(path)
    current_content = None
    if file_exists:
        with open(path, 'r') as f:
            current_content = f.read()

    # Decide if we need to change
    needs_update = not file_exists or current_content != content

    if module.check_mode:
        module.exit_json(changed=needs_update, path=path)

    if needs_update:
        with open(path, 'w') as f:
            f.write(content)
        result['changed'] = True

    result['path'] = path
    module.exit_json(**result)

def main():
    run_module()


if __name__ == '__main__':
    main()
