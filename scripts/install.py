from brownie.project.compiler import install_solc

def compiler():
    install_solc("0.8.12")

if __name__ == "__main__":
    compiler()
