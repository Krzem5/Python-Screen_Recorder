import cv2
import numpy
import ctypes
import ctypes.wintypes


CAPTUREBLT=0x40000000
DIB_RGB_COLORS=0
SRCCOPY=0x00CC0020



class BITMAPINFOHEADER(ctypes.Structure):
	_fields_=[("biSize",ctypes.wintypes.DWORD),("biWidth",ctypes.wintypes.LONG),("biHeight",ctypes.wintypes.LONG),("biPlanes",ctypes.wintypes.WORD),("biBitCount",ctypes.wintypes.WORD),("biCompression",ctypes.wintypes.DWORD),("biSizeImage",ctypes.wintypes.DWORD),("biXPelsPerMeter",ctypes.wintypes.LONG),("biYPelsPerMeter",ctypes.wintypes.LONG),("biClrUsed",ctypes.wintypes.DWORD),("biClrImportant",ctypes.wintypes.DWORD)]



class BITMAPINFO(ctypes.Structure):
	_fields_=[("bmiHeader",BITMAPINFOHEADER),("bmiColors",ctypes.wintypes.DWORD*3)]



S=(3840,2160)
FPS=5



out=cv2.VideoWriter("./cap2.mp4",cv2.VideoWriter_fourcc(*"mp4v"),FPS,S)
ctypes.windll.shcore.SetProcessDpiAwareness(2)
dc=ctypes.windll.user32.GetWindowDC(0)
mm_dc=ctypes.windll.gdi32.CreateCompatibleDC(dc)
bmi=BITMAPINFO()
bmi.bmiHeader.biSize=ctypes.sizeof(BITMAPINFOHEADER)
bmi.bmiHeader.biPlanes=1
bmi.bmiHeader.biBitCount=32
bmi.bmiHeader.biCompression=0
bmi.bmiHeader.biClrUsed=0
bmi.bmiHeader.biClrImportant=0
bmi.bmiHeader.biWidth=S[0]
bmi.bmiHeader.biHeight=-S[1]
dt=ctypes.create_string_buffer(S[0]*S[1]*4)
bmp=ctypes.windll.gdi32.CreateCompatibleBitmap(dc,S[0],S[1])
ctypes.windll.gdi32.SelectObject(mm_dc,bmp)
_TEMP=type("ArrI",(object,),{"__init__":lambda s,dt:setattr(s,"dt",dt),"__array_interface__":property(lambda s:{"version":3,"shape":(S[1],S[0],4),"typestr":"|u1","data":s.dt})})
while True:
	ctypes.windll.gdi32.BitBlt(mm_dc,0,0,S[0],S[1],dc,0,0,SRCCOPY|CAPTUREBLT)
	ctypes.windll.gdi32.GetDIBits(mm_dc,bmp,0,S[1],dt,bmi,DIB_RGB_COLORS)
	frame=numpy.array(_TEMP(bytearray(dt)))
	frame=cv2.cvtColor(frame,cv2.COLOR_RGBA2RGB)
	cv2.imshow("Cap",frame)
	out.write(frame)
	if (cv2.waitKey(int(1/30*1000))&0xff==27):
		break
cv2.destroyAllWindows()
out.release()
