#!/data/data/com.termux/files/usr/bin/bash

echo "🚀 Menjalankan DIABLO_CLICK_ENGINE..."
nohup python bot.py > nohup.out 2>&1 &
sleep 2
echo "📜 Log bot (tekan Ctrl+C untuk keluar tampilan log):"
tail -f nohup.out