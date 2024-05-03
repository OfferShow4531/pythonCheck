import subprocess
import sys

if "google.colab" in sys.modules:
    subprocess.run("apt-get update", shell=True, check=True)
    subprocess.run("apt-get install -qq xvfb libgl1-mesa-glx", shell=True, check=True)
    subprocess.run("pip install pyvista[all] -qq", shell=True, check=True)

    import pyvista as pv

    # Seems that only static plotting is supported by colab at the moment
    pv.global_theme.jupyter_backend = "static"
    pv.global_theme.notebook = True
    pv.start_xvfb()
else:
    from pyvista import set_plot_theme

    set_plot_theme("document")