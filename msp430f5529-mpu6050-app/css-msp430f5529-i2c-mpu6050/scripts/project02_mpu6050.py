"""
 Simulation of a rotating and moving mpu6050 sensor
 Developed by: 
"""
import sys, math, pygame, serial, time
from threading import Thread
from operator import itemgetter

# Temperature
Temp = 0
# accel current value
Ax = 0
Ay = 0
Az = 0
# gyro current value
Gx = 0
Gy = 0
Gz = 0
# gyro past value
Gpx = 0
Gpy = 0
Gpz = 0
# gyro callibration 
GxC = 0
GyC = 0
GzC = 0
# g force 
aGFx = 0
aGFy = 0
aGFz = 0
# rotation
gRx = 0
gRy = 0
gRz = 0
# window of time 
current_time = 0
past_time = 0
# angle for each dimension
AngX = 0
AngY = 0
AngZ = 0
# initialized
initialized = False

def uart_handshake(port):
    ok = b''
    while ok.strip() != b'0':
        port.write(b"1")
        ok = port.read()

def callibrate_gyro(port):
    global GxC,GyC,GzC,Gx,Gy,Gz,initialized
    for x in range(5):
        uart_handshake(port)
        get_sensor_data(port)
        GxC = GxC + Gx
        GyC = GyC + Gy
        GzC = GzC + Gz
    # compute average of the error
    GxC = GxC / 5
    GyC = GyC / 5
    GzC = GzC / 5
    initialized = True

def get_sensor_data(port):
    global Gpx,Gpy,Gpz,Temp,Ax,Ay,Az,Gx,Gy,Gz,aGFx,aGFy,aGFz,gRx,gRy,gRz,past_time,current_time
    Gpx = Gx
    Gpy = Gy
    Gpz = Gz
    # get window of time
    past_time = current_time
    current_time = int(round(time.time() * 1000))
    # load data from uart
    Tempt = port.read(2) 
    Ax = port.read(2)
    Ay = port.read(2)
    Az = port.read(2)
    Gx = port.read(2)
    Gy = port.read(2)
    Gz = port.read(2)
    # temp values, from datasheet
    Temp = (int.from_bytes(Tempt,byteorder = 'big', signed = True) / 340.00) + 36.53
    # accel values
    Ax = (int.from_bytes(Ax,byteorder = 'big', signed = True))
    Ay = (int.from_bytes(Ay,byteorder = 'big', signed = True))
    Az = (int.from_bytes(Az,byteorder = 'big', signed = True))
    # gyro values
    Gx = (int.from_bytes(Gx,byteorder = 'big', signed = True))
    Gy = (int.from_bytes(Gy,byteorder = 'big', signed = True))
    Gz = (int.from_bytes(Gz,byteorder = 'big', signed = True))
    # G force
    aGFx = Ax / 131
    aGFy = Ay / 131
    aGFz = Az / 131
    # Angular
    gRx = Gx / 16384
    gRy = Gy / 16384
    gRz = Gz / 16384
        
def calculate_angle():
    global AngX,AngY,AngZ,current_time,past_time
    # same equation can be written as 
    # angelZ = angelZ + ((timePresentZ - timePastZ)*(gyroZPresent + gyroZPast - 2*gyroZCalli)) / (2*1000*131);
    # 1/(1000*2*131) = 0.00000382
    # 1000 --> convert milli seconds into seconds
    # 2 --> comes when calculation area of trapezium
    # substacted the callibated result two times because there are two gyro readings
    time_delta = (current_time - past_time)
    AngX = AngX + (time_delta * (Gx + Gpx - 2*GxC)) * 0.00000382
    AngY = AngY + (time_delta * (Gy + Gpy - 2*GyC)) * 0.00000382
    AngZ = AngZ + (time_delta * (Gz + Gpz - 2*GzC)) * 0.00000382


def get_data():
    global current_time,past_time,AngX,AngY,AngZ
    print("Connecting to serial port ...")
    port = serial.Serial(port = 'COM5',
                     baudrate = 115200,
                     #baudrate = 9600,
                     bytesize = serial.EIGHTBITS,
                     parity   = serial.PARITY_NONE,
                     stopbits = serial.STOPBITS_ONE,
                     timeout=1)
    print("Connected!!")
    callibrate_gyro(port);
    while True:
        uart_handshake(port)
        get_sensor_data(port)
        calculate_angle()
        print("T = %.3f | Ax = %.3f, Ay = %.3f, Az = %.3f | Gx = %.3f, Gy = %.3f, Gz = %.3f" % (Temp,aGFx,aGFy,aGFz,gRx,gRy,gRz))
        print("Time = %d | Agx = %.3f, Agy = %.3f, Agz = %.3f" % (current_time > past_time,AngX,AngY,AngZ))

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
 
    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)
 
    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)
 
    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)
 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, self.z)
 
class Simulation:
    def __init__(self, win_width = 640, win_height = 480):
        pygame.init()
 
        self.screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption("Simulation of a MPU6050 sensor (CIATEQ-SIM-Compilers)")
        
        self.clock = pygame.time.Clock()
 
        self.vertices = [
            Point3D(-1,1,-1),
            Point3D(1,1,-1),
            Point3D(1,-1,-1),
            Point3D(-1,-1,-1),
            Point3D(-1,1,1),
            Point3D(1,1,1),
            Point3D(1,-1,1),
            Point3D(-1,-1,1)
        ]
 
        # Define the vertices that compose each of the 6 faces. These numbers are
        # indices to the vertices list defined above.
        self.faces  = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]
 
        # Define colors for each face
        self.colors = [(100,200,200),(100,200,240),(100,240,200),(100,240,240),(100,100,200),(100,200,100)]
 
        self.angle = 0
        
    def temp2color(self,t):
        if t > 40:
            t = 38
        if t < 0:
            t = 1
        return (255 * (t/40))

    def run(self):
        """ Main Loop """
        global initialized,AngX,AngY,AngZ,Temp
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
 
            self.clock.tick(200)
            self.screen.fill((180,180,180))
 
            # It will hold transformed vertices.
            t = []
 
            for v in self.vertices:
                # Rotate the point around X axis, then around Y axis, and finally around Z axis.
                r = v.rotateX(-AngX).rotateY(-AngZ).rotateZ(-AngY)
                # Transform the point from 3D to 2D
                p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
                # Put the point in the list of transformed vertices
                t.append(p)
            self.colors  = [(self.temp2color(Temp), color[1], color[2]) for color in self.colors]
            # Calculate the average Z values of each face.
            avg_z = []
            i = 0
            for f in self.faces:
                z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
                avg_z.append([i,z])
                i = i + 1
 
            # Draw the faces using the Painter's algorithm:
            # Distant faces are drawn before the closer ones.
            for tmp in sorted(avg_z,key=itemgetter(1),reverse=True):
                face_index = tmp[0]
                f = self.faces[face_index]
                pointlist = [(t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),
                             (t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y),
                             (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y),
                             (t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y)]
                pygame.draw.polygon(self.screen,self.colors[face_index],pointlist)
 
            pygame.display.flip()
 
if __name__ == "__main__":
    communication = Thread(target=get_data)
    communication.daemon = True
    communication.start()
    
    Simulation().run()
