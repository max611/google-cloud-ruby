# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.gcp as gcp
import synthtool.languages.ruby as ruby
import logging
from subprocess import call

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()

v1alpha2 = gapic.ruby_library(
    'irm', 'v1alpha2',
    artman_output_name='google-cloud-ruby/google-cloud-irm',
    config_path='artman_irm_v1alpha2.yaml'
)
s.copy(v1alpha2 / 'lib')
s.copy(v1alpha2 / 'test')
s.copy(v1alpha2 / 'README.md')
s.copy(v1alpha2 / 'LICENSE')
s.copy(v1alpha2 / '.gitignore')
s.copy(v1alpha2 / '.yardopts')
s.copy(v1alpha2 / 'google-cloud-irm.gemspec', merge=ruby.merge_gemspec)

# Copy common templates
templates = gcp.CommonTemplates().ruby_library()
s.copy(templates)

# Support for service_address
s.replace(
    [
        'lib/google/cloud/irm.rb',
        'lib/google/cloud/irm/v*.rb',
        'lib/google/cloud/irm/v*/*_client.rb'
    ],
    '\n(\\s+)#(\\s+)@param exception_transformer',
    '\n\\1#\\2@param service_address [String]\n' +
        '\\1#\\2  Override for the service hostname, or `nil` to leave as the default.\n' +
        '\\1#\\2@param service_port [Integer]\n' +
        '\\1#\\2  Override for the service port, or `nil` to leave as the default.\n' +
        '\\1#\\2@param exception_transformer'
)
s.replace(
    [
        'lib/google/cloud/irm/v*.rb',
        'lib/google/cloud/irm/v*/*_client.rb'
    ],
    '\n(\\s+)metadata: nil,\n\\s+exception_transformer: nil,\n',
    '\n\\1metadata: nil,\n\\1service_address: nil,\n\\1service_port: nil,\n\\1exception_transformer: nil,\n'
)
s.replace(
    [
        'lib/google/cloud/irm/v*.rb',
        'lib/google/cloud/irm/v*/*_client.rb'
    ],
    ',\n(\\s+)lib_name: lib_name,\n\\s+lib_version: lib_version',
    ',\n\\1lib_name: lib_name,\n\\1service_address: service_address,\n\\1service_port: service_port,\n\\1lib_version: lib_version'
)
s.replace(
    'lib/google/cloud/irm/v*/*_client.rb',
    'service_path = self\\.class::SERVICE_ADDRESS',
    'service_path = service_address || self.class::SERVICE_ADDRESS'
)
s.replace(
    'lib/google/cloud/irm/v*/*_client.rb',
    'port = self\\.class::DEFAULT_SERVICE_PORT',
    'port = service_port || self.class::DEFAULT_SERVICE_PORT'
)
s.replace(
    'google-cloud-irm.gemspec',
    '\n  gem\\.add_dependency "google-gax", "~> 1\\.[\\d\\.]+"\n',
    '\n  gem.add_dependency "google-gax", "~> 1.7"\n')

# https://github.com/googleapis/gapic-generator/issues/2243
s.replace(
    'lib/google/cloud/irm/*/*_client.rb',
    '(\n\\s+class \\w+Client\n)(\\s+)(attr_reader :\\w+_stub)',
    '\\1\\2# @private\n\\2\\3')

# https://github.com/googleapis/gapic-generator/issues/2279
s.replace(
    'lib/**/*.rb',
    '\\A(((#[^\n]*)?\n)*# (Copyright \\d+|Generated by the protocol buffer compiler)[^\n]+\n(#[^\n]*\n)*\n)([^\n])',
    '\\1\n\\6')

# https://github.com/googleapis/gapic-generator/issues/2323
s.replace(
    [
        'lib/**/*.rb',
        'README.md'
    ],
    'https://github\\.com/GoogleCloudPlatform/google-cloud-ruby',
    'https://github.com/googleapis/google-cloud-ruby'
)
s.replace(
    [
        'lib/**/*.rb',
        'README.md'
    ],
    'https://googlecloudplatform\\.github\\.io/google-cloud-ruby',
    'https://googleapis.github.io/google-cloud-ruby'
)

# https://github.com/googleapis/gapic-generator/issues/2393
s.replace(
    'google-cloud-irm.gemspec',
    'gem.add_development_dependency "rubocop".*$',
    'gem.add_development_dependency "rubocop", "~> 0.64.0"'
)

# Require the helpers file
s.replace(
    f'lib/google/cloud/irm/v1alpha2.rb',
    f'require "google/cloud/irm/v1alpha2/incident_service_client"',
    '\n'.join([
        f'require "google/cloud/irm/v1alpha2/incident_service_client"',
        f'require "google/cloud/irm/v1alpha2/helpers"',
    ])
)

s.replace(
    'google-cloud-irm.gemspec',
    '"README.md", "LICENSE"',
    '"README.md", "AUTHENTICATION.md", "LICENSE"'
)
s.replace(
    '.yardopts',
    'README.md\n',
    'README.md\nAUTHENTICATION.md\nLICENSE\n'
)

# https://github.com/googleapis/google-cloud-ruby/issues/3058
s.replace(
    'google-cloud-irm.gemspec',
    '\nGem::Specification.new do',
    'require File.expand_path("../lib/google/cloud/irm/version", __FILE__)\n\nGem::Specification.new do'
)
s.replace(
    'google-cloud-irm.gemspec',
    '(gem.version\s+=\s+).\d+.\d+.\d.*$',
    '\\1Google::Cloud::Irm::VERSION'
)
s.replace(
    'lib/google/cloud/irm/v1alpha2/*_client.rb',
    '(require \".*credentials\"\n)\n',
    '\\1require "google/cloud/irm/version"\n\n'
)
s.replace(
    'lib/google/cloud/irm/v1alpha2/*_client.rb',
    'Gem.loaded_specs\[.*\]\.version\.version',
    'Google::Cloud::Irm::VERSION'
)

# Generate the helper methods
call('bundle update && bundle exec rake generate_partials', shell=True)