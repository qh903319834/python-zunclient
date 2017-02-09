#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json

from tempest.lib.common.utils import data_utils
from tempest.lib import exceptions

from zunclient.tests.functional import base


class TestCase(base.FunctionalTestBase):

    def openstack(self, *args, **kwargs):
        return self._zun_osc(*args, **kwargs)

    def get_opts(self, fields=None, output_format='json'):
        """Get options for OSC output fields format.

        :param List fields: List of fields to get
        :param String output_format: Select output format
        :return: String of formatted options
        """
        if not fields:
            return ' -f {0}'.format(output_format)
        return ' -f {0} {1}'.format(output_format,
                                    ' '.join(['-c ' + it for it in fields]))

    def container_create(self, image='cirros', name=None, params=''):
        """Create container and add cleanup.

        :param String image: Image for a new container
        :param String name: Name for a new container
        :param String params: Additional args and kwargs
        :return: JSON object of created container
        """
        if not name:
            name = data_utils.rand_name('container')

        opts = self.get_opts()
        output = self.openstack('appcontainer create {0}'
                                ' {1} --name {2} {3}'
                                .format(opts, image, name, params))
        container = json.loads(output)

        if not output:
            self.fail('Container has not been created!')
        return container

    def container_delete(self, identifier, ignore_exceptions=False):
        """Try to delete container by name or UUID.

        :param String identifier: Name or UUID of the container
        :param Bool ignore_exceptions: Ignore exception (needed for cleanUp)
        :return: raw values output
        :raise: CommandFailed exception when command fails
                to delete a container
        """
        try:
            return self.openstack('appcontainer delete {0}'
                                  .format(identifier))
        except exceptions.CommandFailed:
            if not ignore_exceptions:
                raise

    def container_list(self, fields=None, params=''):
        """List Container.

        :param List fields: List of fields to show
        :param String params: Additional kwargs
        :return: list of JSON node objects
        """
        opts = self.get_opts(fields=fields)
        output = self.openstack('appcontainer list {0} {1}'
                                .format(opts, params))
        return json.loads(output)

    def container_show(self, identifier, fields=None, params=''):
        """Show specified baremetal node.

        :param String identifier: Name or UUID of the node
        :param List fields: List of fields to show
        :param List params: Additional kwargs
        :return: JSON object of node
        """
        opts = self.get_opts(fields)
        output = self.openstack('appcontainer show {0} {1} {2}'
                                .format(opts, identifier, params))
        return json.loads(output)