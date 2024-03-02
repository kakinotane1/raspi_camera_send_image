python -m venv --system-site-packages .venv_picamera

source .venv_picamera/bin/activate

pip install -U pip
pip install -r requirements.txt

# install picamera
# pip install git+https://github.com/waveform80/picamera

deactivate