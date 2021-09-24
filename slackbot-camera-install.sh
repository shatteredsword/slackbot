sudo apt install python3-pip python3-picamera
CAMERA=$(sudo raspi-config nonint get_camera)
if [[ "$CAMERA" -ne "0" ]]; then
    sudo raspi-config nonint do_camera 0
fi
sudo cp camera/camera.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable camera && sudo systemctl start camera && sudo systemctl status camera
