#!/bin/bash
chmod -R +x robot_pi_service/
sudo groupadd gpio
sudo usermod -aG gpio $USER
echo 'SUBSYSTEM=="gpio", KERNEL=="gpiochip[0-9]*", GROUP="gpio", MODE="0660"' | sudo tee /etc/udev/rules.d/99-gpio.rules
sudo udevadm control --reload-rules
sudo udevadm trigger