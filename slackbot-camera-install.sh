sudo apt install python3-pip
pip3 install --user pipenv
CAMERA=$(sudo raspi-config nonint get_camera)
if [[ "$CAMERA" -ne "0" ]]; then
    sudo raspi-config nonint do_camera 0
fi
sudo cp camera/camera.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable camera && sudo systemctl start camera
sleep 5s
sudo systemctl status camera
