# All Rights Reserved.
#
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

import jsonschema
import mock

from rally.task import exporter
from tests.unit import test


class ExporterTestCase(test.TestCase):

    def setUp(self):
        super(ExporterTestCase, self).setUp()

        @exporter.configure(name="test-exporter")
        class FakeExporter(exporter.Exporter):

            def validate(self):
                pass

            def export(self, task, connection_string):
                pass

        self.FakeExporter = FakeExporter
        self.addCleanup(FakeExporter.unregister)

    def test_task_export(self):
        self.assertRaises(TypeError, exporter.Exporter, "fake_connection")

    def test_task_export_instantiate(self):
        self.FakeExporter("fake_connection")


class TaskExporterTestCase(test.TestCase):

    def test_make(self):
        reporter_cls = mock.Mock()

        reporter_cls.return_value.generate.return_value = {}
        exporter.TaskExporter.make(reporter_cls, None, None, None)

        reporter_cls.return_value.generate.return_value = {"files": {}}
        exporter.TaskExporter.make(reporter_cls, None, None, None)
        reporter_cls.return_value.generate.return_value = {
            "files": {"/path/foo": "content"}}
        exporter.TaskExporter.make(reporter_cls, None, None, None)

        reporter_cls.return_value.generate.return_value = {"open": "/path/foo"}
        exporter.TaskExporter.make(reporter_cls, None, None, None)

        reporter_cls.return_value.generate.return_value = {"print": "foo"}
        exporter.TaskExporter.make(reporter_cls, None, None, None)

        reporter_cls.return_value.generate.return_value = {
            "files": {"/path/foo": "content"}, "open": "/path/foo",
            "print": "foo"}
        exporter.TaskExporter.make(reporter_cls, None, None, None)

        reporter_cls.return_value.generate.return_value = {"files": []}
        self.assertRaises(jsonschema.ValidationError,
                          exporter.TaskExporter.make,
                          reporter_cls, None, None, None)

        reporter_cls.return_value.generate.return_value = {"files": ""}
        self.assertRaises(jsonschema.ValidationError,
                          exporter.TaskExporter.make,
                          reporter_cls, None, None, None)

        reporter_cls.return_value.generate.return_value = {"files": {"a": {}}}
        self.assertRaises(jsonschema.ValidationError,
                          exporter.TaskExporter.make,
                          reporter_cls, None, None, None)

        reporter_cls.return_value.generate.return_value = {"open": []}
        self.assertRaises(jsonschema.ValidationError,
                          exporter.TaskExporter.make,
                          reporter_cls, None, None, None)

        reporter_cls.return_value.generate.return_value = {"print": []}
        self.assertRaises(jsonschema.ValidationError,
                          exporter.TaskExporter.make,
                          reporter_cls, None, None, None)

        reporter_cls.return_value.generate.return_value = {"additional": ""}
        self.assertRaises(jsonschema.ValidationError,
                          exporter.TaskExporter.make,
                          reporter_cls, None, None, None)
