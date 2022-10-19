import os
import shutil
from tempfile import mkdtemp
from unittest.mock import patch

import pytest
from traitlets import Integer

from jupyter_core.application import JupyterApp, NoStart

pjoin = os.path.join


def test_basic():
    JupyterApp()


def test_default_traits():
    app = JupyterApp()
    for trait_name in app.traits():
        getattr(app, trait_name)


class DummyApp(JupyterApp):
    name = "dummy-app"
    m = Integer(0, config=True)
    n = Integer(0, config=True)


_dummy_config = """
c.DummyApp.n = 10
"""


def test_custom_config():
    app = DummyApp()
    td = mkdtemp()
    fname = pjoin(td, "config.py")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(_dummy_config)
    app.initialize(["--config", fname])
    shutil.rmtree(td)
    assert app.config_file == fname
    assert app.n == 10


def test_cli_override():
    app = DummyApp()
    td = mkdtemp()
    fname = pjoin(td, "config.py")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(_dummy_config)
    app.initialize(["--config", fname, "--DummyApp.n=20"])
    shutil.rmtree(td)
    assert app.n == 20


def test_generate_config():
    td = mkdtemp()
    app = DummyApp(config_dir=td)
    app.initialize(["--generate-config"])
    assert app.generate_config

    with pytest.raises(NoStart):
        app.start()

    assert os.path.exists(os.path.join(td, "dummy_app_config.py"))






def test_runtime_dir_changed():
    app = DummyApp()
    td = mkdtemp()
    shutil.rmtree(td)
    app.runtime_dir = td
    assert os.path.isdir(td)
    shutil.rmtree(td)
