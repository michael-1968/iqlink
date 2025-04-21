

class Figuredefinition():
    def __init__(self, name, element1, element2, element3):
        self.Name = name
        self.Geometrie = {"Name": name, "Element1": element1, "Element2": element2,"Element3": element3}
        self.element1_type = self.Geometrie['Element1'].get('Type', '')
        self.element2_type = self.Geometrie['Element2'].get('Type', '')
        self.element3_type = self.Geometrie['Element3'].get('Type', '')
        self.element1_open = self.Geometrie['Element1'].get('Open', '')
        self.element2_open = self.Geometrie['Element2'].get('Open', '')
        self.element3_open = self.Geometrie['Element3'].get('Open', '')
        self.element1_angle = '' if element1.get('Angle', '') == "" else '^'
        self.element2_angle = '' if element2.get('Angle', '') == "" else '^'
        self.element3_angle = '' if element3.get('Angle', '') == "" else '^'

        self.Useage = self.calculate_Useage()
          
    def get(self):
        return self.Geometrie
    
    def calculate_Useage(self):
        usage = 0
        if (self.element1_type == "X"):
            usage += 1
        if (self.element3_type == "X"):
            usage += 1
        if (self.element2_type == "Y"):
            usage += 1
        else:
            usage += len(self.element2_open)    
        usage += len(self.element1_open)    
        usage += len(self.element3_open)    
        return usage
    
    def useage(self):
        return self.Useage
        
    def __str__(self):
        # Ensure all elements have the 'Type' key
        returnstring = (
            f"{self.Geometrie['Name']}" +
            f" - {self.element1_angle}{self.element1_type}" + 
            f"{self.element2_angle}{self.element2_type}" + 
            f"{self.element3_type}{self.element3_angle}" +
            f" - {self.Useage}"
        )
        return returnstring

def nameToGeometry(name):
    if name == "Blau":
        return Blau
    if name == "Rot":
        return Rot
    if name == "Bordeaux":
        return Bordeaux
    if name == "Orange":
        return Orange
    if name == "Dunkelviolet":
        return Dunkelviolet
    if name == "Dunkelgruen":
        return Dunkelgruen
    if name == "Gruen":
        return Gruen
    if name == "Hellgruen":
        return Hellgruen
    if name == "Violet":
        return Violet
    if name == "Gelb":
        return Gelb
    if name == "Hellblau":
        return Hellblau
    if name == "Magenta":
        return Magenta
    raise Exception(f'Figure.openAngles: Problem with definition - name:{name}')

Blau = Figuredefinition("Blau", {"Type": "C", "Open": [300]}, 
                {"Type": "Y", "Open": [60, 120, 180, 240] }, 
                {"Type": "X", "Angle": 300})

Rot  = Figuredefinition("Rot", {"Type": "X", "Angle": 120}, 
                {"Type": "C", "Open": [0]}, 
                {"Type": "C", "Open": [300]})

Bordeaux  = Figuredefinition("Bordeaux", {"Type": "X", "Angle": 60}, 
                {"Type": "C", "Open": [0]}, 
                {"Type": "X"})

Orange  = Figuredefinition("Orange", {"Type": "X", "Angle": 120}, 
                {"Type": "C", "Open": [0]}, 
                {"Type": "X"})

Dunkelviolet  = Figuredefinition("Dunkelviolet", {"Type": "X", "Angle": 60}, 
                {"Type": "O"}, 
                {"Type": "C", "Open": [300]})

Dunkelgruen  = Figuredefinition("Dunkelgruen", {"Type": "X"}, 
                {"Type": "O"}, 
                {"Type": "C", "Open": [240]})

Gruen  = Figuredefinition("Gruen", {"Type": "C", "Open": [0]}, 
                {"Type": "Y", "Open": [60, 120, 180, 240]}, 
                {"Type": "X", "Angle": 300})

Hellgruen  = Figuredefinition("Hellgruen", {"Type": "X"}, 
                {"Type": "O"}, 
                {"Type": "C", "Open": [300]})

Violet  = Figuredefinition("Violet", {"Type": "X"}, 
                {"Type": "C", "Open": [240, 300]}, 
                {"Type": "X"})

Gelb  = Figuredefinition("Gelb", {"Type": "C", "Open": [0], "Angle": 60}, 
                {"Type": "O"}, 
                {"Type": "C", "Open": [300], "Angle": 300})

Hellblau  = Figuredefinition("Hellblau", {"Type": "X", "Angle": 300}, 
                {"Type": "O"}, 
                {"Type": "C", "Open": [240]})

Magenta  = Figuredefinition("Magenta", {"Type": "X", "Angle": 300}, 
                {"Type": "O"}, 
                {"Type": "C", "Open": [300]})

