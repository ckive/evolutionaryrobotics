from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, rgba):

        self.depth  = 3
        color_str = " ".join(str(c) for c in rgba)
        self.string1 = f'<material name="{color_str}">'

        self.string2 = f'    <color rgba="{color_str}"/>'

        self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )

