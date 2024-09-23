# How to packaging for Pypi

> https://packaging.python.org/tutorials/packaging-projects/

## Project Structure

In venv, no `--user` needed for PIP.

1. Prepare files: `setup.py`, `LICENSE`, and `README.md`.
2. Prepare directory: `tests`.
3. Setup uploader with PYPI account.
    1. Ensure ` ~/.pypirc` with token.
    2. `python3 -m pip install --upgrade setuptools wheel`
    3. `python3 setup.py sdist bdist_wheel`
4. Upload the `dist` files with Twine to [testpypi](https://test.pypi.org/project/nehushtan/).
    1. `python3 -m pip install --upgrade twine`
    2. Upload to Test.Pypi: `python3 -m twine upload --repository testpypi dist/*`
5. Test installing.
    1. `python3 -m pip install --index-url https://test.pypi.org/simple/ --upgrade nehushtan`
6. Publish to [pypi](https://pypi.org/project/nehushtan/)
    1. `python3 -m twine upload dist/*`
7. Installing.
    1. `pip3 install nehushtan`

