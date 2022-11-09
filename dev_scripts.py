import subprocess


def build_html_docs():
    cmd = "poetry run mkdocs build > docs_print.html".split(" ")
    subprocess.run(cmd)
