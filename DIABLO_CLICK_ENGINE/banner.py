#!/usr/bin/env python3
"""Tampilan banner DIABLO_CLICK_ENGINE dengan ASCII, statistik, dan petunjuk."""

from pyfiglet import Figlet

# ANSI color codes
RED = "\033[91m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
RESET = "\033[0m"
BOLD = "\033[1m"

SKULL = r'''
      .ed""" """$$$be.
    -"           ^""**$$$e.
  ."                   '$$$c
 /                      "4$$b
/                        d$$$
|                         $$$
'             .eeeeee.    $$$
  .          ""    ""   .$$$
   ".                 .$$$$
     "-.._____..-"$$$$$$"
'''


def show_banner(valid: int, total: int, ip: str, durasi: float) -> None:
    """Cetak tampilan skull + judul DIABLO dan informasi statistik bot."""
    fig = Figlet(font="slant")
    diablo_text = fig.renderText("DIABLO")

    print(f"{RED}{SKULL}{RESET}")
    print(f"{MAGENTA}{diablo_text}{RESET}")

    print(f"{BOLD}{CYAN}🔹 IP Lokal  : {WHITE}{ip}{RESET}")
    print(f"{BOLD}{CYAN}⏱️  Durasi    : {WHITE}{durasi:.2f} detik{RESET}")
    print(f"{BOLD}{CYAN}🌐 Proxy OK : {WHITE}{valid}/{total}{RESET}")
    print(f"{BOLD}{GREEN}✅ BOT SIAP JALAN!{RESET}\n")

    print(f"{YELLOW}📌 Ketik {BOLD}bash start.sh{RESET}{YELLOW} untuk memulai ulang bot jika perlu.")
    print(f"🔗 Masukkan link shortlink satu per satu lalu ketik '{BOLD}DONE{RESET}{YELLOW}'.")
    print(f"📥 Contoh: {WHITE}https://shortlink.com/abc123{RESET}\n")