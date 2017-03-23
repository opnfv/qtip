- Which framework has been used and why
- How to extend to more commands

Original content from DEVELOP.md

    ### CLI

    Click currently supports Bash completion. The prerequisite for this is that the program
    needs to be installed correctly. To install Qtip, execute the following command in root
    folder of Qtip:

    ```
    cd <project root>
    pip install -e .
    ```

    Once the installation has been completed successfully, the following needs to be added to
    the `.bashrc` file:

    ```
    eval "$(_QTIP_COMPLETE=source qtip)"
    ```

    The above would activate command completion for Qtip.
