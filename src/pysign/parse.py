"""
Module for parsing segmented HamNoSys transcriptions.
"""
from pysign.data import HAMNOSYS

def ascify(text, sep='.'):
    return '.'.join(
            HAMNOSYS.get(char, {"Name": '<'+char+'>'})["Name"] for char in
            text).replace('.asciispace.', ' ')

def parse_hamnosys(text, 
        symmetry_base="", 
        handshape_base="",
        handshape_diacritic="",
        orientation_base="",
        orientation_diacritic="",
        brush="",
        location_base="",
        location_diacritic="",
        contact_base="",
        movement_base="",
        movement_diacritic="",
        ambiguous_diacritic="",
        open_bracket="",
        open_par="",
        close_par="",
        dominance_meta="",
        close_bracket="",
        ascify_text=False
        ):
    
    in_symmetry, symmetry = False, []
    in_handshape, handshapes, handshapes_meta = False, [], []
    in_brush, in_contact, contact = False, False, []
    in_location, location, location_meta = False, [], []
    in_orientation, orientation, orientation_meta = False, [], []
    in_movement, movement, movement_meta = False, [], []
    rest = ''
    for i, char in enumerate(text):
        # start with characters unique to symmetry
        if char in symmetry_base:
            in_symmetry = True 
            symmetry += [char]
        # next, characters unique to handshape
        elif char in handshape_base:
            in_symmetry = False # turn off; won't pick up ambiguous diacritics
            in_handshape = True
            handshapes += [char]
        elif char in handshape_diacritic:
            handshapes[-1] += char
        #next, characters unique to orientation
        elif char in orientation_base:
            in_handshape = False
            if in_orientation:
                orientation[-1] += char # can be two base characters in sequence
            else:
                in_orientation = True 
                orientation += [char]
        elif char == orientation_diacritic: 
            orientation[-1] += char
        # brush and contact symbols can be separated, but should be joined
        elif char == brush: 
            in_handshape = False # in case handshape changes switch on
            in_orientation = False # in case orientation changes switch on
            in_brush = True # to join with contact after intervening location
            contact += [char]
        # next, characters unique to location
        elif char in location_base:
            in_handshape = False
            in_orientation = False            
            if in_location:
                location[-1] += char # can be two base characters in sequence
            else:
                in_location = True 
                location += [char]
        elif char in location_diacritic: 
            location[-1] += char
        # next, characters unique to contact
        elif char in contact_base:
            in_location = False
            if in_brush: 
                in_brush = False
                in_contact = True
                contact[-1] += char
            else:    
                in_contact = True
                contact += [char]
        # next, characters unique to movement
        elif char in movement_base:
            in_contact = False
            in_location = False
            if in_movement:
                movement[-1] += char 
            else:
                in_movement = True 
                movement += [char] 
        elif char in movement_diacritic: 
            movement[-1] += char
        # some diacritics can occur in most environments
        elif char in ambiguous_diacritic: 
            if in_symmetry:
                symmetry[-1] += char
            elif in_handshape:
                handshapes[-1] += char
            elif in_orientation:
                orientation[-1] += char
            elif in_contact:
                contact[-1] += char
            elif in_location:
                location[-1] += char
            else:
                movement[-1] += char
        # meaning of open bracket can't be predicted
        elif char == open_bracket:
            if text[i+1] in handshape_base: # check the next character
                handshapes_meta += char
            elif text[i+1] in orientation_base:
                orientation_meta += char
            elif text[i+1] in contact_base:
                location_meta += char
            elif text[i+1] in location_base:
                location_meta += char
            elif text[i+1] in movement_base:
                movement_meta += char
            elif text[i+1] == open_bracket:
                movement_meta += char  
            elif text[i+1] == open_par: # grouping symbols in 2-handed signs
                if text[i+2] in handshape_base: # check two characters ahead
                    handshapes_meta += char
                elif text[i+2] in orientation_base:
                    orientation_meta += char
                elif text[i+2] in contact_base:
                    location_meta += char
                elif text[i+2] in location_base:
                    location_meta += char
                elif text[i+2] in movement_base: 
                    movement_meta += char
                else:
                    rest += char
            else:
                rest += char
        # marker for 2-handed sign
        elif char == dominance_meta: 
            if dominance_meta not in handshapes_meta:
                handshapes_meta += char
            elif dominance_meta not in orientation_meta:
                in_orientation = False # next orientation symbol should be added as new segment
                orientation_meta += char
            elif dominance_meta not in location_meta:
                in_location = False
                location_meta += char
            else:
                in_movement = False
                movement_meta += char
        # assign close brackets
        elif char == close_bracket:
            if close_bracket not in handshapes_meta:
                handshapes_meta += char
            elif close_bracket not in orientation_meta:
                in_orientation = False
                orientation_meta += char
            elif close_bracket not in location_meta:
                in_location = False
                location_meta += char
            elif close_bracket not in movement_meta:
                movement_meta += char
            else:
                in_movement = False
                movement_meta += char
        # grouping symbol can occur in most environments
        elif char == open_par:
            if text[i+1] in handshape_base: # check the next character
                handshapes_meta += char
            elif text[i+1] in orientation_base:
                orientation_meta += char
            elif text[i+1] in contact_base:
                location_meta += char
            elif text[i+1] in location_base:
                location_meta += char
            else:
                movement_meta += char
        # grouping symbol can occur in most environments; todo: more than one set in environment
        elif char == close_par:
            if close_par not in handshapes_meta:
                handshapes_meta += char
            elif close_par not in orientation_meta:
                in_orientation = False
                orientation_meta += char
            elif close_par not in location_meta:
                in_location = False
                location_meta += char
            elif close_par not in movement_meta:
                movement_meta += char
            else:
                in_movement = False
                movement_meta += char
        else:
            rest += char

    # handshapes
    # check for symmetry
    if symmetry != []:
        if dominance_meta not in handshapes_meta:
            # dominant and nondominant are the same
            dominant_hand = handshapes[0]
            nondominant_hand = handshapes[0]
            handshape_change = ''.join(handshapes[1:])
        # symmetry is for other segment type
        else:
            dominant_hand = handshapes[0]
            nondominant_hand = ''.join(handshapes[1])
            handshape_change = ''.join(handshapes[2:])            
    # determine dominant hand, no symmetry
    elif dominance_meta in handshapes_meta:
        dominant_hand = handshapes[0]
        nondominant_hand = ''.join(handshapes[1])
        handshape_change = ''.join(handshapes[2:])
    # one hand, no symmetry
    else:
        dominant_hand = handshapes[0]
        nondominant_hand = ''
        handshape_change = ''.join(handshapes[1:])

    # orientation
    if symmetry != []:
        # in fact, this is much more complex; +++to do+++
        if dominance_meta not in orientation_meta:
            dominant_orientation = orientation[0]
            nondominant_orientation = orientation[0]
            orientation_change = ''.join(orientation[1:])
        else:
            dominant_orientation = orientation[0]
            nondominant_orientation = ''.join(orientation[1])
            orientation_change = ''.join(orientation[2:])            
    # determine dominant orientation
    elif dominance_meta in orientation_meta:
        dominant_orientation = orientation[0]
        nondominant_orientation = ''.join(orientation[1])
        orientation_change = ''.join(orientation[2:])
    # only one hand
    else:
        dominant_orientation = orientation[0]
        nondominant_orientation = ''
        orientation_change = ''.join(orientation[1:])

    # location
    if symmetry != []:
        # in fact, this is much more complex; +++to do+++
        if dominance_meta not in location_meta:
            dominant_location = location[0]
            nondominant_location = location[0]
            location_change = ''.join(location[1:])
        else:
            dominant_location = location[0]
            nondominant_location = ''.join(location[1])
            location_change = ''.join(location[2:])            
    # determine dominant location
    elif dominance_meta in location_meta:
        dominant_location = location[0]
        nondominant_location = ''.join(location[1])
        location_change = ''.join(location[2:])
    # only one hand
    else:
        dominant_location = location[0]
        nondominant_location = ''
        location_change = ''.join(location[1:])

    # movement
    if symmetry != []:
        # in fact, this is much more complex; +++to do+++
        if dominance_meta not in movement_meta:
            dominant_movement = movement[0]
            nondominant_movement = movement[0]
            movement_change = ''.join(movement[1:])
        else:
            dominant_movement = movement[0]
            nondominant_movement = ''.join(movement[1])
            movement_change = ''.join(movement[2:])            
    # determine dominant movement
    elif dominance_meta in movement_meta:
        dominant_movement = movement[0]
        nondominant_movement = ''.join(movement[1])
        movement_change = ''.join(movement[2:])
    # only one hand
    else:
        dominant_movement = movement[0]
        nondominant_movement = ''
        movement_change = ''.join(movement[1:])
    
    # check bracketing for simultaneous movement
    if movement_meta.count(open_bracket) > 1:
        dominant_movement = open_bracket + dominant_movement + close_bracket
    elif movement_meta.count(open_bracket) > 2:
        dominant_movement = open_bracket + dominant_movement + close_bracket
        movement_change = open_bracket + movement_change + close_bracket
    else:
        pass

    if not ascify_text:
        data = {
                'symmetry': symmetry,
                'handshape': {
                    'dominant': {
                        'shape': dominant_hand,
                        'change': handshape_change
                        },
                    'nondominant': {
                        'shape': nondominant_hand,
                        'change': '' # is this never annotated?
                        },
                    },
                'orientation': { 
                    'dominant': {
                        'orientation': dominant_orientation,
                        'change': orientation_change
                        },
                    'nondominant': {
                        'orientation': nondominant_orientation,
                        'change': '' # is this never annotated?
                        },
                    },
                'contact': contact,
                'location': { 
                    'dominant': {
                        'location': dominant_location,
                        'change': location_change
                        },
                    'nondominant': {
                        'location': nondominant_location
                        },
                    },
                'movement': { 
                    'dominant': {
                        'movement': dominant_movement,
                        'change': movement_change
                        },
                    'nondominant': {
                        'movement': nondominant_movement
                        },
                    },                
#                'errors': unparsable,
                'handshape metasymbols': handshapes_meta,
                'orientation metasymbols': orientation_meta,
                'location metasymbols': location_meta,
                'movement metasymbols': movement_meta,
                'rest': rest
               }
    else:
        data = {
                'symmetry': ascify(symmetry),
                'handshape': {
                    'dominant': {
                        'shape': ascify(dominant_hand),
                        'change': ascify(handshape_change)
                        },
                    'nondominant': {
                        'shape': ascify(nondominant_hand),
                        'change': '' # is this never annotated?
                        },
                    },
                'orientation': {
                    'dominant': {
                        'orientation': ascify(dominant_orientation),
                        'change': ascify(orientation_change)
                        },
                    'nondominant': {
                        'orientation': ascify(nondominant_orientation),
                        'change': '' # is this never annotated?
                        },
                    },
                'contact': ascify(contact),
                'location': { 
                    'dominant': {
                        'location': ascify(dominant_location),
                        'change': ascify(location_change)
                        },
                    'nondominant': {
                        'location': ascify(nondominant_location)
                        },
                    },                
                'movement': { 
                    'dominant': {
                        'movement': ascify(dominant_movement),
                        'change': ascify(movement_change)
                        },
                    'nondominant': {
                        'movement': ascify(nondominant_movement)
                        },
                    },                
#                'errors': ascify(unparsable),
                'handshape metasymbols': ascify(handshapes_meta),
                'orientation metasymbols': ascify(orientation_meta),
                'location metasymbols': ascify(location_meta),
                'movement metasymbols': ascify(movement_meta),
                'rest': ascify(rest)
                }
    return data

             


class Word(object):
    
    def __init__(self, text, delimiter=' + '):
        self.signs = [Sign(sign) for sign in text.split(delimiter)]


class Sign(object):

    def __init__(self, text, delimiter=None):
        
        segments = text.split(delimiter)
        data = {}
        for i, segment in enumerate(segments):
            pass


