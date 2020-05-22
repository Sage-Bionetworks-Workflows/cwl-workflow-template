import unittest
import yaml

from utils import bump_cwl_version

class TestBumpCwlVersion(unittest.TestCase):


  def test_parse_docker_image_happy_paths(self):
    fake_image_name = 'organization/repository:v1.0.0'
    test_data = [
      # test hints as dictionary
      (
        {'hints': {'DockerRequirement': {'dockerPull': fake_image_name }}},
        {'docker_requirement_found_in': 'hints', 'object_type': dict}
      ),
      # test hints as list
      (
        {'hints': [{'class': 'DockerRequirement','dockerPull': fake_image_name}]},
        {'docker_requirement_found_in': 'hints', 'object_type': list}
      ),
      # test requiremments as dictionary
      (
        {'requirements': {'DockerRequirement': {'dockerPull': fake_image_name }}},
        {'docker_requirement_found_in': 'requirements', 'object_type': dict}
      ),
      # test requirements as list
      (
        {'requirements': [{'class': 'DockerRequirement', 'dockerPull': fake_image_name}]},
        {'docker_requirement_found_in': 'requirements', 'object_type': list}
      )
    ]
    for test_datum in test_data:
      tool = test_datum[0]
      expected_metadata = test_datum[1]
      docker_image, parsing_metadata = bump_cwl_version.parse_docker_image(tool)
      self.assertEqual(docker_image, fake_image_name)
      for k,v in parsing_metadata.items():
        expected_metadata[k] = v


  def test_parse_docker_image_unhappy_paths(self):
    test_data = [
      (
        bump_cwl_version.ERROR_UNEXPECTED_TYPE,
        {'hints': 0}
      ),
      (
        bump_cwl_version.ERROR_MISSING_DOCKER_REQUIREMENT,
        {'hints': {}}
      ),
      (
        bump_cwl_version.ERROR_MISSING_DOCKER_PULL,
        {'hints': {'DockerRequirement': {}}}
      )
    ]
    for test_datum in test_data:
      expected_error = test_datum[0]
      tool = test_datum[1]
      with self.assertRaises(ValueError) as context_manager:
        bump_cwl_version.parse_docker_image(tool)
      error_message = str(context_manager.exception)
      self.assertEqual(error_message, expected_error)


  def test_edit_tool(self):
    original_fake_image_name = 'organization/repository:v1.0.0'
    new_version = 'v1.0.1'
    final_fake_image_name = 'organization/repository:v1.0.1'
    test_data = [
      (
        {'hints': {'DockerRequirement': {'dockerPull': original_fake_image_name }}},
        {'hints': {'DockerRequirement': {'dockerPull': final_fake_image_name }}}
      ),
      # test hints as list
      (
        {'hints': [{'class': 'DockerRequirement','dockerPull': original_fake_image_name}]},
        {'hints': [{'class': 'DockerRequirement','dockerPull': final_fake_image_name}]}
      ),
      # test requiremments as dictionary
      (
        {'requirements': {'DockerRequirement': {'dockerPull': original_fake_image_name }}},
        {'requirements': {'DockerRequirement': {'dockerPull': final_fake_image_name }}}
      ),
      # test requirements as list
      (
        {'requirements': [{'class': 'DockerRequirement', 'dockerPull': original_fake_image_name}]},
        {'requirements': [{'class': 'DockerRequirement', 'dockerPull': final_fake_image_name}]}
      )
    ]
    for test_datum in test_data:
      tool = test_datum[0]
      expected_tool = test_datum[1]
      new_tool = bump_cwl_version.edit_tool(tool, new_version)
      self.assertEqual(new_tool, yaml.dump(expected_tool))
