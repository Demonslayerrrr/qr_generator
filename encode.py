unicode_string = "茗"
unicode_string2 = "荷"
shift_jis_encoded = unicode_string.encode('shift_jis').hex()
shift_jis_encoded2 = unicode_string2.encode('shift_jis').hex()

print(shift_jis_encoded, shift_jis_encoded2)


print(f"0x{(0x89D7 - 0x8140):04X}")
