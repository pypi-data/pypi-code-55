import os
import re
import tempfile
import shutil
import functools

exe_dir = os.path.dirname(os.path.realpath(__file__))
test_datadir = os.path.join(exe_dir, "data", "test_mv")
code_dir = os.path.join(test_datadir, "code")
yaml_file = os.path.join(test_datadir, "scikick.yml")
# get scikick cli name
#exec(open(os.path.join(exe_dir, "cli_name.py")).read())
cli_name = "sk"

htmls = ["code/analysis_normalization.html", 
	"code/analysis_summary.html", "index.html", "code/test_python.html",
	"code/data_generate.html", "code/test_bash.html"]

html_init = ["code/analysis_normalization.html", "code/analysis_summary.html",
	"code/data_generate.html"]

html_ren = ["code/analysis_norm.html", "code/analysis_summ.html",
	"code/data_gen.html"]

class TestMv:
	# copy test project to a separate temporary directory
	def setup(self):
		self.project_dir = tempfile.TemporaryDirectory()
		shutil.copytree(code_dir, os.path.join(self.project_dir.name, "code"))
		shutil.copy2(yaml_file, self.project_dir.name)
		# go to the project dir, where scikick will be run
		os.chdir(self.project_dir.name)
		os.system("git init")
		os.system("git add *")
	# delete the tmpdir/everything that was created
	def teardown(self):
		self.project_dir.cleanup()
	# running scikick with different arguments
	def test_mv1(self):
		for i in range(0, len(html_init)):
			hi = re.sub(".html", "", html_init[i])
			hr = re.sub(".html", "", html_ren[i])
			os.system("%s mv %s.Rmd %s.Rmd" % (cli_name, hi, hr))
		os.system("%s run" % cli_name)
		#os.system('pwd')
		#while 1:print("A")
		html_dir = os.path.join("report", "out_html")
		assert os.path.isdir(html_dir)
		for curr_file in html_init:
			assert not os.path.isfile(os.path.join(html_dir, curr_file))
		for curr_file in html_ren:
			assert os.path.isfile(os.path.join(html_dir, curr_file))
	def test_mv2(self):
		for i in range(0, len(html_init)):
			hi = re.sub(".html", "", html_init[i])
			hr = re.sub(".html", "", html_ren[i])
			os.system("%s mv -g %s.Rmd %s.Rmd" % (cli_name, hi, hr))
		os.system("%s run" % cli_name)
		html_dir = os.path.join("report", "out_html")
		assert os.path.isdir(html_dir)
		for curr_file in html_init:
			assert not os.path.isfile(os.path.join(html_dir, curr_file))
		for curr_file in html_ren:
			assert os.path.isfile(os.path.join(html_dir, curr_file))
	def test_mv3(self):
		for i in range(0, len(html_init)):
			hi = re.sub(".html", "", html_init[i])
			hr = re.sub(".html", "", html_ren[i])
			os.system("%s mv -g %s.Rmd %s.Rmd" % (cli_name, hi, hr))
		os.system("%s run" % cli_name)
		html_dir = os.path.join("report", "out_html")
		assert os.path.isdir(html_dir)
		for curr_file in html_init:
			assert not os.path.isfile(os.path.join(html_dir, curr_file))
		for curr_file in html_ren:
			assert os.path.isfile(os.path.join(html_dir, curr_file))
