import pyrosim.pyrosim as pyrosim

length = 1
width = 1
height = 1

x,y,z = 0, 0, 0.5

pyrosim.Start_SDF("boxes.sdf")
for i in range(5):
    for j in range(5):
        for k in range(10):
            poses = [x+i, y+j, z+k]
            sizes = [0.9**k*length, 0.9**k*width, 0.9**k*height]
            pyrosim.Send_Cube(name="Box", pos=poses , size=sizes)

pyrosim.End()