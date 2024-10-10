import copy
import opsc
import oobb
import oobb_base

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    # save_type variables
    if True:
        filter = ""
        #filter = "test"

        kwargs["save_type"] = "none"
        #kwargs["save_type"] = "all"
        
        kwargs["overwrite"] = True
        
        #kwargs["modes"] = ["3dpr", "laser", "true"]
        kwargs["modes"] = ["3dpr"]
        #kwargs["modes"] = ["laser"]

    # default variables
    if True:
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 3
        
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        part_default = {} 
        part_default["project_name"] = "test" ####### neeeds setting
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        p3["width"] = 3
        p3["height"] = 3
        p3["thickness"] = 20
        part["kwargs"] = p3
        
        part["name"] = "bracket_corner"
        parts.append(part)

        
    #make the parts
    if True:
        for part in parts:
            name = part.get("name", "default")
            if filter in name:
                print(f"making {part['name']}")
                make_scad_generic(part)            
                print(f"done {part['name']}")
            else:
                print(f"skipping {part['name']}")

def get_base(thing, **kwargs):

    depth = kwargs.get("thickness", 4)
    depth += 3
    prepare_print = kwargs.get("prepare_print", False)

    pos = kwargs.get("pos", [0, 0, 0])
    #pos = copy.deepcopy(pos)
    #pos[2] += -20

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    #add holes
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = "perimeter"
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

def get_bracket_corner(thing, **kwargs):

    depth = kwargs.get("thickness", 4)
    depth_of_extra_piece = 3
    depth += depth_of_extra_piece
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    prepare_print = kwargs.get("prepare_print", False)

    pos = kwargs.get("pos", [0, 0, 0])
    #pos = copy.deepcopy(pos)
    #pos[2] += -20

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    # add cutout for item
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"oobb_cube"
    shif = 14
    wid = (width * 15) - shif
    hei = (height * 15) - shif
    dep = depth - depth_of_extra_piece
    p3["size"] = [wid,hei,dep]
    pos1 = copy.deepcopy(pos)
    pos1[0] += shif/2
    pos1[1] += shif/2
    pos1[2] += 0    
    p3["pos"] = pos1
    #p3["m"] = "#"
    oobb_base.append_full(thing,**p3)


    #add holes m3
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["radius_name"] = "m3"
    p3["depth"] = depth
    p3["holes"] = "perimeter"
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add holes m6
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"oobb_holes"
    p3["radius_name"] = "m6"
    p3["depth"] = depth
    p3["holes"] = "single"
    #make an array that has all positions in a matrix width and height
    locations = []
    for x in range(1,width+1):
        for y in range(1,height+1):
            locations.append([x,y])
    #remove [1,1], [width,1], [1,height]
    locations.remove([1,1])
    locations.remove([width,1])
    locations.remove([1,height])
    #add the holes
    p3["locations"] = locations

    #p3["m"] = "#"
    oobb_base.append_full(thing,**p3)


    #add screw holes 1,1, 1,height, width,1
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m3d5_screw_wood"
    p3["depth"] = depth
    #p3["m"] = "#"
    poss_oobb = [1,1],[1,height],[width,1]
    poss = []
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth
    for pos in poss_oobb:
        pos11 = copy.deepcopy(pos1)
        pos11[0] += (pos[0]) * 15 - width/2 * 15 - 15/2
        pos11[1] += (pos[1]) * 15 - height/2 * 15 - 15/2
        poss.append(pos11)
    p3["pos"] = poss
    oobb_base.append_full(thing,**p3)




    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

###### utilities



def make_scad_generic(part):
    
    # fetching variables
    name = part.get("name", "default")
    project_name = part.get("project_name", "default")
    
    kwargs = part.get("kwargs", {})    
    
    modes = kwargs.get("modes", ["3dpr", "laser", "true"])
    save_type = kwargs.get("save_type", "all")
    overwrite = kwargs.get("overwrite", True)

    kwargs["type"] = f"{project_name}_{name}"

    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")

    #get the part from the function get_{name}"
    func = globals()[f"get_{name}"]    
    # test if func exists
    if callable(func):            
        func(thing, **kwargs)        
    else:            
        get_base(thing, **kwargs)   
    

    for mode in modes:
        depth = thing.get(
            "depth_mm", thing.get("thickness_mm", 3))
        height = thing.get("height_mm", 100)
        layers = depth / 3
        tilediff = height + 10
        start = 1.5
        if layers != 1:
            start = 1.5 - (layers / 2)*3
        if "bunting" in thing:
            start = 0.5
        opsc.opsc_make_object(f'scad_output/{thing["id"]}/{mode}.scad', thing["components"], mode=mode, save_type=save_type, overwrite=overwrite, layers=layers, tilediff=tilediff, start=start)    


if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)