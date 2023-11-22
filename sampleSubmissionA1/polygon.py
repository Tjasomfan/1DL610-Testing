
def polygon(nodes):
    if isinstance(nodes,list):
        if len(nodes) <= 2:
            result = "Not a polygon"
        elif len(nodes) == 3:
            result = triang(nodes[0], nodes[1], nodes[2])
        elif len(nodes) == 4:
            result = quadrilateral(nodes[0], nodes[1], nodes[2], nodes[3])
        else:
            print("This is a large polygon")
            result = "Large Polygon"
        return result
    else:
        return "Input is not a list"

def triang(n1,n2,n3):
    if n1==n2==n3:
        return "Equilateral"
    elif n1==n2 or n2==n3 or n3==n1:
        return "Isosceles"
    else:
        return "Scalene"

def quadrilateral(n1,n2,n3,n4):
    if n1==n2==n3==n4:
        return "Square"
    elif (n1==n3 and n2==n4) or (n1==n2 and n3==n4) or (n1==n4 and n2==n3):
        return "Rectangle"
    else:
        return "Irregular Quadrilateral"