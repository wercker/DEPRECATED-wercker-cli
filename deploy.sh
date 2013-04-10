echo "[server-login]" >> ~/.pypirc
echo "username:" $PYPI_USER >> ~/.pypirc
echo "password:" $PYPI_PASSWORD >> ~/.pypirc
pwd
ls -la
python setup.py sdist upload
