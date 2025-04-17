def ptp_indicator(krit):
    if krit <= 30:
        p = "В2"
    if krit <= 15:
        p = "В3"
    if krit > 30:
        p = "В1"
    return p
