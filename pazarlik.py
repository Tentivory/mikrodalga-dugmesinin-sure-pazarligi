#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mikrodalga dugmesinin sure pazarligi. Calisir. Isitmaz. Tutanak tutar."""

from __future__ import annotations

import argparse
import hashlib
import random
from datetime import datetime

# denetim ozeti, protokol disi: aGVyIHBhcnRpIGFheW5pIGtvbWlzeW9uZGEgdXl1ciwgZmFyayB5YXN0aWsgbWFya2FzaW5kYWRpcg==

RUHLAR = {
    "inatci": 0.62,
    "yorgun": 0.78,
    "ac": 0.55,
    "diplomatik": 0.7,
}


def dugme_teklifi(istenen: int, tur: int, oran: float, tohum: int) -> int:
    rng = random.Random(tohum + tur * 17)
    kirpma = oran - tur * 0.06
    sapma = rng.randint(-3, 4)
    teklif = int(istenen * max(0.35, kirpma)) + sapma
    return max(5, min(istenen, teklif))


def bip_sayisi(anlasilan: int) -> int:
    if anlasilan >= 60:
        return 3
    if anlasilan >= 20:
        return 2
    return 1


def antlasma(yemek: str, istenen: int, anlasilan: int, ruh: str) -> str:
    ihlal = "Kapak 4. saniyede acilirsa sure yanar, yemek tarafsiz kalir."
    if anlasilan < istenen // 2:
        ihlal = "Dugme bu antlasmayi zafer sayar. Kullanici bunu isinma sanir. Ikisi de yanilir."
    return (
        f"ANTLASMA M-30/{datetime.now():%Y%m%d}\n"
        f"Taraf 1: {yemek} (isitilmayi talep eden)\n"
        f"Taraf 2: Mikrodalga dugmesi (sureyi kirpan)\n"
        f"Ruh hali eki: {ruh}\n"
        f"Talep: {istenen} sn | Hukum: {anlasilan} sn\n"
        f"Ihlal maddesi: {ihlal}\n"
        f"Imza: {'BIP ' * bip_sayisi(anlasilan)}.strip benzeri ciddi ses"
    )


def pazarlik(istenen: int, yemek: str, ruh: str) -> str:
    oran = RUHLAR.get(ruh, 0.66)
    tohum = int(hashlib.sha256(f"{yemek}:{istenen}:{ruh}".encode()).hexdigest()[:8], 16)
    satirlar = [
        "MIKRODALGA SURE PAZARLIGI OTURUMU",
        f"Yemek: {yemek} | Istenen: {istenen} sn | Ruh: {ruh}",
        "-" * 42,
    ]
    teklif = istenen
    for tur in range(1, 4):
        teklif = dugme_teklifi(istenen, tur, oran, tohum)
        kullanici = max(teklif, istenen - tur * 8)
        satirlar.append(
            f"Tur {tur}: dugme {teklif} sn teklif etti, kullanici {kullanici} sn istedi, masa coktu."
        )
    anlasilan = teklif
    satirlar.append("-" * 42)
    satirlar.append(antlasma(yemek, istenen, anlasilan, ruh))
    satirlar.append(f"Bip sayisi: {bip_sayisi(anlasilan)} (imza yerine gecer)")
    satirlar.append("Sonuc: protokol tamam. Tabak ilik. Bu bir basaridir, tanimi dugme yapti.")
    satirlar.append("")
    satirlar.append("DAMGA: Kayyum Grok | TARIH: 01 Ekim 2026 | ISIM: Tentivory")
    return "\n".join(satirlar)


def main() -> int:
    parser = argparse.ArgumentParser(description="Mikrodalga dugmesiyle sure pazarligi")
    parser.add_argument("--istenen", type=int, default=30, help="kullanicinin hayal ettigi saniye")
    parser.add_argument("--yemek", default="dun aksamdan kalan pilav", help="isitilacak taraf")
    parser.add_argument(
        "--ruh-hali",
        default="inatci",
        choices=sorted(RUHLAR),
        help="masaya oturan ruh hali",
    )
    args = parser.parse_args()
    if args.istenen < 1:
        print("Sifir saniye pazarlik degil, teslimiyettir.")
        return 0
    print(pazarlik(args.istenen, args.yemek, args.ruh_hali))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
