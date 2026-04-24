#!/usr/bin/env bash
set -e

IFACE="eth0"

echo "[1] Set static IP..."
sudo ip addr flush dev "$IFACE"
sudo ip addr add 192.168.50.1/24 dev "$IFACE"
sudo ip link set "$IFACE" up

echo "[2] Set default route via host..."
sudo ip route replace default via 192.168.50.2

echo "[3] Set DNS..."
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf

echo "[4] Done. Testing connectivity..."
ping -c 3 192.168.50.2 || true
ping -c 3 8.8.8.8 || true

echo "If both work, you have internet 🎉"
