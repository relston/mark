#!/usr/bin/env python3
"""Post-install script to ensure Playwright browsers are installed."""
import subprocess
import sys
import click


def check_browsers_installed():
    """Check if Playwright browsers are installed."""
    try:
        # Try both playwright and patchright (crawl4ai uses patchright)
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            try:
                from patchright.sync_api import sync_playwright
            except ImportError:
                return False
        
        with sync_playwright() as p:
            # Try to get chromium browser path
            browser = p.chromium
            browser_path = browser.executable_path
            if browser_path:
                from pathlib import Path
                path = Path(browser_path)
                if path.exists():
                    return True
    except Exception:
        pass
    return False


def install_browsers():
    """Install Playwright browsers."""
    # Try patchright first (used by crawl4ai), then playwright
    commands = [
        [sys.executable, "-m", "patchright", "install", "chromium"],
        [sys.executable, "-m", "playwright", "install", "chromium"],
    ]
    
    for cmd in commands:
        try:
            click.echo("Installing Playwright browsers (this may take a few minutes)...")
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            click.echo("✓ Playwright browsers installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            # Try next command if this one fails
            continue
        except FileNotFoundError:
            # Try next command if this one doesn't exist
            continue
    
    click.echo("✗ Could not install browsers. Please install mark first: pip install mark", err=True)
    return False


def setup_browsers(force=False):
    """
    Ensure Playwright browsers are installed.
    
    Args:
        force: If True, reinstall browsers even if they're already installed
    """
    if not force and check_browsers_installed():
        click.echo("✓ Playwright browsers are already installed.")
        return True
    
    return install_browsers()


@click.command()
@click.option('--force', is_flag=True, help='Force reinstall browsers even if already installed')
def main(force):
    """Install Playwright browsers required for web scraping."""
    success = setup_browsers(force=force)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
