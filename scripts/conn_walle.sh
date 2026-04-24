#sudo nmcli connection modify "Wired connection 1" \
#  ipv4.method manual \
#  ipv4.addresses 192.168.50.2/24 \
#  ipv4.gateway "" \
#  ipv4.dns ""
#sudo nmcli connection down "Wired connection 1"
#sudo nmcli connection up "Wired connection 1"
#ssh pi@192.168.50.1
#!/usr/bin/env bash
set -e

CONN="Wired connection 1"
LAN_IF="eth0"      # interface to Pi
WAN_IF="wlan0"     # interface with internet

echo "[1] Configure static IP on LAN..."
sudo nmcli connection modify "$CONN" \
  ipv4.method manual \
  ipv4.addresses 192.168.50.2/24 \
  ipv4.gateway "" \
  ipv4.dns ""

echo "[2] Restart connection..."
sudo nmcli connection down "$CONN" || true
sudo nmcli connection up "$CONN"

echo "[3] Enable IP forwarding..."
sudo sysctl -w net.ipv4.ip_forward=1

# Persist it
if ! grep -q "net.ipv4.ip_forward=1" /etc/sysctl.conf; then
  echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
fi

echo "[4] Set up NAT (iptables)..."
sudo iptables -t nat -C POSTROUTING -o "$WAN_IF" -j MASQUERADE 2>/dev/null || \
sudo iptables -t nat -A POSTROUTING -o "$WAN_IF" -j MASQUERADE

sudo iptables -C FORWARD -i "$WAN_IF" -o "$LAN_IF" -m state --state RELATED,ESTABLISHED -j ACCEPT 2>/dev/null || \
sudo iptables -A FORWARD -i "$WAN_IF" -o "$LAN_IF" -m state --state RELATED,ESTABLISHED -j ACCEPT

sudo iptables -C FORWARD -i "$LAN_IF" -o "$WAN_IF" -j ACCEPT 2>/dev/null || \
sudo iptables -A FORWARD -i "$LAN_IF" -o "$WAN_IF" -j ACCEPT

# 1. Enable forwarding
sudo sysctl -w net.ipv4.ip_forward=1

# 2. Clear any broken rules
sudo iptables -F
sudo iptables -t nat -F

# 3. Add correct NAT + forwarding
sudo iptables -t nat -A POSTROUTING -o wlo1 -j MASQUERADE

sudo iptables -A FORWARD -i wlo1 -o enp46s0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i enp46s0 -o wlo1 -j ACCEPT

echo "[5] Done. You can now SSH:"
echo "    ssh pi@192.168.50.1"
