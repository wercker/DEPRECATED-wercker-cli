import os
import shutil

from werckercli.cli import get_term, puts

from werckercli import prompt
from werckercli.paths import find_git_root

import json

def validate():
	term = get_term()
	git_root_path = find_git_root(os.curdir)

	if not git_root_path:
		puts(term.red("Error: ") + "Could not find a git")
		return

	wercker_json_path = os.path.join(git_root_path, "wercker.json")
	if os.path.exists(wercker_json_path) is False:
		puts(term.yellow("Warning: ") +" Could not find a wercker.json file")
		return

	if os.path.getsize(wercker_json_path) == 0:
		puts(term.red("Error: ") + "wercker.json is found, but empty")
		return

	try:
		with open(wercker_json_path) as f:
			try:
				json.load(f)
			except ValueError as e:
				puts(term.red("Error: ") + "wercker.json is not valid json: " + e.message)
	except IOError as e:
		puts(term.red("Error: ") + "Error while reading wercker.json file: " + e.message)