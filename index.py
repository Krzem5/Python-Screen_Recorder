import cv2
import mss
import numpy



S=(3840,2160)
FPS=5



with mss.mss() as sc:
	out=cv2.VideoWriter("./cap2.mp4",cv2.VideoWriter_fourcc(*"mp4v"),FPS,S)
	while True:
		frame=numpy.array(sc.grab({"top":0,"left":0,"width":S[0],"height":S[1]}))
		frame=cv2.cvtColor(frame,cv2.COLOR_RGBA2RGB)
		cv2.imshow("Cap",frame)
		out.write(frame)
		if (cv2.waitKey(int(1/30*1000))&0xff==27):
			break
cv2.destroyAllWindows()
out.release()