# Note: this script is called during docker build to
# pre-download solc at Docker image build time, so it
# will be immediately available when the container starts.

from brownie.project.compiler import install_solc

if __name__ == "__main__":
    install_solc("0.8.12")
