import os
import shutil
import subprocess
from tempfile import TemporaryDirectory

import glob


header = """
\\documentclass{article}
\\usepackage{xcolor}
\\begin{document}
"""

footer = """
\\end{document}
"""


def highlight(text: list, color_opacities: list, target_file: str, color="red", max_opacity=1.0, tex_executable="pdflatex", verbose=False):

    percentages = [min(int(round((op / max_opacity) * 100)), 100) for op in color_opacities]
    colored_strings = [r"\colorbox{%s!%s}{\strut{%s}}" % (color, perc, word) for word, perc in zip(text, percentages)]

    doc = header + " ".join(colored_strings) + footer
    
    # Generate tex file in temporary directory to not need to cleanup after the generation process
    with TemporaryDirectory() as tmp_dir:
        tmp_file = os.path.join(tmp_dir, "tmpfile.tex")
        with open(tmp_file, "w") as fh:
            fh.write(doc)
            
        subprocess.run([tex_executable, tmp_file], cwd=tmp_dir, capture_output=not verbose)
                
        pdf_file = os.path.join(tmp_dir, "tmpfile.pdf")
        shutil.copy(pdf_file, target_file)


if __name__ == "__main__":
    import random
    text = """Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod 
    tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. 
    At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, 
    no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, 
    consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore 
    magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea 
    rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."""
    
    words = [word.strip() for word in text.split(" ") if word.strip()]
    opacities = [random.random() for _ in words]
    
    highlight(words, opacities, "tmp.pdf", verbose=False, color="red", max_opacity=1.0)
    
