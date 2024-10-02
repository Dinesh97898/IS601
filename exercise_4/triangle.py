class Triangle:

    #Constructor
    def __init__(self,base,height) -> None:
        self.height = height
        self.base = base

    # __str__ function
    def __str__(self) -> str:
        return f"Triangle: base={self.base}, height={self.height}"
    
    #calculate Hypoteuse
    def hypotenuse(self):
        return (self.base**2 + self.height**2)**0.5
    
    #calculate area
    def area(self):
        return (1/2)*self.height*self.base
    
    


