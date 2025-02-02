import os
import subprocess
import sys


def create_venv(venv_dir):
    """Creates a virtual environment in the specified directory."""
    print(f"Creating virtual environment in {venv_dir}...")
    subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
    print(f"Virtual environment created in {venv_dir}.")


def install_requirements(venv_dir, requirements_file=None):
    """Installs dependencies from a requirements.txt file (if provided)."""
    if requirements_file and os.path.exists(requirements_file):
        print(f"Installing dependencies from {requirements_file}...")
        subprocess.run(
            [os.path.join(venv_dir, "bin", "pip"), "install", "-r", requirements_file],
            check=True,
        )
        print("Dependencies installed.")
    else:
        print("No requirements file found, skipping dependency installation.")


def create_gitignore():
    """Creates a .gitignore file with common Python ignores."""
    gitignore_content = """
# Ignore the .env file
.env
 
# Ignore the archive folder
archive/
 
# Ignore the virtual environment folder and any config files
venv/
.venv/
my_env/
config.py

# Byte-compiled / optimized / DLL files / log files
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.pyc 
 
# Flask and Gunicorn logs
*.log
*.out
*.err

# macOS and Linux system files
.DS_Store
Thumbs.db



# Ignore figures
figures/

# Ignore chroma db
chroma_db/

# Ignore input folders
input_files/
uploads/

# Ignore backup-repo
backup-repo/

# Pytest cache and coverage reports
.pytest_cache/
.coverage
.tox/
nosetests.xml
coverage.xml
*.cover
*.py,cover
htmlcov/

# Docker files and folders (if using Docker)
docker-compose.override.yml
.dockerignore

# IDEs and editors (optional, add specific files based on your setup)
.vscode/
.idea/
*.sublime-project
*.sublime-workspace

# Python egg files
*.egg
*.egg-info/
dist/
build/
eggs/
parts/
sdist/
develop-eggs/
.installed.cfg
lib/
lib64/

"""
    gitignore_path = ".gitignore"
    with open(gitignore_path, "w") as f:
        f.write(gitignore_content)
    print(f".gitignore file created at {gitignore_path}.")


def main():
    # Step 1: Set up the virtual environment directory
    project_dir = os.getcwd()  # Current working directory
    venv_dir = os.path.join(project_dir, "venv")

    # Create the virtual environment
    if not os.path.exists(venv_dir):
        create_venv(venv_dir)
    else:
        print(f"Virtual environment already exists in {venv_dir}. Skipping creation.")

    # Step 2: Install dependencies if a requirements.txt file exists
    requirements_file = "requirements.txt"
    install_requirements(venv_dir, requirements_file)

    # Step 3: Create .gitignore file
    create_gitignore()

    print("Project setup complete!")


if __name__ == "__main__":
    main()
