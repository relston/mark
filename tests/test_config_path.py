import os

from mark import config as config_mod


def test_relative_config_path_stays_under_cwd(tmp_path, monkeypatch):
    """A relative MARK_CONFIG_PATH must resolve under the working directory."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("MARK_CONFIG_PATH", "relcfg-for-test")
    config_mod.reset()
    try:
        cfg = config_mod.Config()
    finally:
        config_mod.reset()
    assert not os.path.isabs(cfg.system_prompts_dir)
    assert cfg.system_prompts_dir == os.path.join("relcfg-for-test", "system_prompts")
    assert os.path.isdir(tmp_path / "relcfg-for-test" / "system_prompts")
    assert os.path.isfile(
        tmp_path / "relcfg-for-test" / "system_prompts" / "default.md"
    )
