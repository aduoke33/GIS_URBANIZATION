from pyproj import Transformer

t = Transformer.from_crs('EPSG:32648', 'EPSG:4326', always_xy=True)

xmin = 561150.0
xmax = 571620.0
ymin = 2346600.0
ymax = 2361060.0

lon_sw, lat_sw = t.transform(xmin, ymin)
lon_nw, lat_nw = t.transform(xmin, ymax)
lon_se, lat_se = t.transform(xmax, ymin)
lon_ne, lat_ne = t.transform(xmax, ymax)

cx = (xmin + xmax) / 2
cy = (ymin + ymax) / 2
clon, clat = t.transform(cx, cy)

def dms(deg, is_lat):
    d = int(deg)
    rem = (deg - d) * 60
    m = int(rem)
    s = (rem - m) * 60
    d_str = 'N' if is_lat else 'E'
    return f"{d}°{m}'{s:.2f}\" {d_str}"

print("=== TOA DO CHI TIET VUNG NGHIEN CUU ===")
print(f"1. Toa do tam (Center):")
print(f"   - Thap phan (Decimal): {clat:.6f}°N, {clon:.6f}°E")
print(f"   - Do phut giay (DMS):  {dms(clat, True)}, {dms(clon, False)}")
print(f"   - UTM Zone 48N:        X = {cx:.1f} m, Y = {cy:.1f} m")
print(f"   - Link Google Maps:    https://www.google.com/maps?q={clat:.6f},{clon:.6f}")
print()
print(f"2. Pham vi gioi han (Bounding Box):")
print(f"   - Vi do (Latitude):    Tu {lat_sw:.6f}°N ({dms(lat_sw, True)}) den {lat_nw:.6f}°N ({dms(lat_nw, True)})")
print(f"   - Kinh do (Longitude): Tu {lon_sw:.6f}°E ({dms(lon_sw, False)}) den {lon_se:.6f}°E ({dms(lon_se, False)})")
print(f"   - UTM Zone 48N:        Easting = [{xmin:.0f} m -> {xmax:.0f} m]")
print(f"                          Northing = [{ymin:.0f} m -> {ymax:.0f} m]")
print()
print(f"3. 4 goc bao khung (4 Corners):")
print(f"   - Tay Nam (South-West): {lat_sw:.6f}°N, {lon_sw:.6f}°E ({dms(lat_sw, True)}, {dms(lon_sw, False)})")
print(f"   - Tay Bac (North-West): {lat_nw:.6f}°N, {lon_nw:.6f}°E ({dms(lat_nw, True)}, {dms(lon_nw, False)})")
print(f"   - Dong Nam (South-East): {lat_se:.6f}°N, {lon_se:.6f}°E ({dms(lat_se, True)}, {dms(lon_se, False)})")
print(f"   - Dong Bac (North-East): {lat_ne:.6f}°N, {lon_ne:.6f}°E ({dms(lat_ne, True)}, {dms(lon_ne, False)})")
print()
print(f"4. Kich thuoc & Dien tich vung nghien cuu:")
print(f"   - Chieu rong (Tay -> Dong): {(xmax - xmin)/1000:.2f} km ({int((xmax-xmin)/30)} cot pixel Landsat 30m)")
print(f"   - Chieu dai (Bac -> Nam):   {(ymax - ymin)/1000:.2f} km ({int((ymax-ymin)/30)} hang pixel Landsat 30m)")
print(f"   - Tong dien tich:           {((xmax - xmin) * (ymax - ymin))/10000:.2f} ha (~{((xmax - xmin) * (ymax - ymin))/1000000:.2f} km2)")

