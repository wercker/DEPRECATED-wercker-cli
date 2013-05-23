echo "[server-login]" >> ~/.pypirc
echo "username:" $PYPI_USER > ~/.pypirc
echo "password:" $PYPI_PASSWORD >> ~/.pypirc
cat ~/.pypirc
python setup.py sdist upload
