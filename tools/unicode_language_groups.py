# Generates a list of language groups for the Unicode CLDR data.

# Maps first 12 bits to the corresponding group
# (Below table is based on https://en.wikipedia.org/wiki/User:Drmccreedy/roadmap)
prefix_map = {
    0x000:'Latin',
    0x030:'Europe',
    0x059:'ME',
    0x078:'AsiaSC',
    0x07C:'Africa',
    0x080:'ME',
    0x090:'AsiaSC',
    0x0E0:'AsiaSE',
    0x0F0:'AsiaSC',
    0x100:'AsiaSE',
    0x10A:'Europe',
    0x110:'AsiaEast',
    0x120:'Africa',
    0x13A:'Americas',
    0x168:'Europe',
    0x170:'IndOcean',
    0x178:'AsiaSE',
    0x180:'AsiaSC',
    0x18B:'Americas',
    0x190:'AsiaSC',
    0x195:'AsiaSE',
    0x1A0:'IndOcean',
    0x1A2:'AsiaSE',
    0x1AB:'Europe',
    0x1B0:'IndOcean',
    0x1C0:'AsiaSC',
    0x1C8:'Europe',
    0x1CC:'IndOcean',
    0x1CD:'AsiaSC',
    0x1D0:'Latin',
    0x1DC:'Europe',
    0x1E0:'Latin',
    0x1F0:'Europe',
    0x207:'symbols',
    0x280:'notation',
    0x290:'symbols',
    0x2C0:'Europe',
    0x2C6:'Latin',
    0x2C8:'Europe',
    0x2D3:'Africa',
    0x2DE:'Europe',
    0x2E0:'symbols',
    0x2E8:'Han',
    0x2FE:'unallocated',
    0x2FF:'Han',
    0x300:'AsiaEast',
    0x31C:'Han',
    0x31F:'AsiaEast',
    0x320:'symbols',
    0x340:'Han',
    0x4DC:'symbols',
    0x4E0:'Han',
    0xA00:'AsiaEast',
    0xA50:'Africa',
    0xA64:'Europe',
    0xA6A:'Africa',
    0xA70:'AsiaEast',
    0xA72:'Latin',
    0xA80:'AsiaSC',
    0xA83:'symbols',
    0xA84:'AsiaSC',
    0xA90:'AsiaSE',
    0xA93:'IndOcean',
    0xA96:'AsiaEast',
    0xA98:'IndOcean',
    0xA9E:'AsiaSE',
    0xAAE:'AsiaSC',
    0xAB0:'Africa',
    0xAB3:'Latin',
    0xAB7:'Americas',
    0xABC:'AsiaSC',
    0xAC0:'AsiaEast',
    0xD80:'surrogates',
    0xF90:'Han',
    0xFB0:'Latin',
    0xFB1:'Europe',
    0xFB2:'ME',
    0xFE0:'variation',
    0xFE1:'AsiaEast',
    0xFE2:'Europe',
    0xFE3:'AsiaEast',
    0xFE7:'ME',
    0xFF0:'AsiaEast',
    0xFFF:'misc',
}
current_group = 'n/a'
languages = {}
print("static char bmp_first_byte_plane0_to_group[0xFFF] = {")
for prefix in range(0x0, 0xFFF):
    if prefix in prefix_map:
        current_group = prefix_map[prefix]
        if current_group not in languages:
            if current_group in ['symbols','misc','variation','unallocated','surrogates','notation']:
                languages[current_group] = 0
            else:
                languages[current_group] = len(languages)+1
    
    if (prefix + 1) % 0x100 == 0:
        print(f'{languages[current_group]},')
    else:
        print(f'{languages[current_group]},', end = '')
print("};")