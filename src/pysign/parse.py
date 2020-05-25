"""
Module for parsing segmented HamNoSys transcriptions.
"""
from pysign.data import HAMNOSYS
import attr
from tabulate import tabulate


def ascify(text, sep='.'):
    return '.'.join(
            HAMNOSYS.get(char, {"Name": '<'+char+'>'})["Name"] for char in
            text).replace('.asciispace.', ' ')

def parse_hamnosys(text,
                   h=True,
                   o=True,
                   c=True,
                   l=True,
                   m=True,
                   ascify_text=False,        
                   ):
    
    # define character types
    symmetry_base=""
    handshape_base=""
    handshape_diacritic=""
    orientation_base=""
    orientation_diacritic=""
    location_base=""
    location_diacritic=""
    contact_base=""
    brush=""
    movement_base=""
    movement_diacritic=""
    repetition=""
    hand_internal_mov=""
    ambiguous_diacritic=""
    ambiguous_location = ""
    open_bracket=""
    open_par=""
    open_fuse=""
    close_par=""
    close_bracket=""
    close_fuse=""
    dominance_meta=""

    # set up environments and variables
    in_symmetry, symmetry = False, []
    in_handshape, handshape, handshapes_meta = False, [], []
    in_orientation, orientation, orientation_meta = False, [], []
    in_location, location, location_meta = False, [], []
    in_initial, initial_position = False, []
    in_brush = False
    in_contact, contact, contact_meta = False, [], []
    in_movement, movement, movement_meta = False, [], []
    in_fusion, in_simultaneous, in_grouped_movement = False, False, False
    in_repetition, in_special_repetition, repeat = False, False, []
    in_hand_internal = False
    rest = ''
    
    for i, char in enumerate(text):
        
        # turn off all environments after space
        if char == ' ':
            in_symmetry = False
            in_handshape = False
            in_orientation = False
            in_contact = False
            in_brush = False
            in_location = False
            in_initial = False
            in_movement = False
            in_fusion = False
            in_simultaneous = False
            in_repetition = False
            in_special_repetition = False
            in_hand_internal = False
            rest += char # not strictly necessary, but just to parse everything
        
        # characters unique to symmetry
        elif char in symmetry_base:
            # turn on symmetry environment
            in_symmetry = True 
            symmetry += [char]
            
        # characters unique to handshape
        elif char in handshape_base:
            in_handshape = True            
            handshape += [char]

            # turn off other environments
            in_symmetry = False 
            in_orientation = False
            in_contact = False
            in_brush = False
            in_location = False
            in_initial = False
            in_repetition = False
            in_special_repetition = False
            in_hand_internal = False
            # leave in_fusion on
            # leave in_simultaneous on
            # leave in_movement on
                    
        elif char in handshape_diacritic:
            handshape[-1] += char
        
        # characters unique to orientation
        elif char in orientation_base:
            # two base characters in sequence
            if in_orientation:
                orientation[-1] += char
            else:
                in_orientation = True 
                orientation += [char]

            # turn off other environments
            in_symmetry = False
            in_handshape = False
            in_contact = False
            in_brush = False
            in_location = False
            in_initial = False
            in_repetition = False
            in_special_repetition = False
            in_hand_internal = False
            # leave in_fusion on
            # leave in_simultaneous on
            # leave in_movement on
                        
        elif char == orientation_diacritic: 
            orientation[-1] += char

        # join brush and contact symbols
        elif char == brush: 
            in_brush = True
            contact += [char]

            # turn off other environments
            in_symmetry = False
            in_handshape = False
            in_orientation = False
            in_contact = False
            in_location = False
            in_initial = False
            in_repetition = False
            in_special_repetition = False
            in_hand_internal = False
            # leave in_fusion on
            # leave in_simultaneous on
            # leave in_movement on

        # characters unique to location
        elif char in location_base:
            # two location base characters in sequence
            if in_location:
                location[-1] += char
            # more detailed transcription for initial position
            elif in_initial:
                initial_position[-1] += char # follows another symbol
            elif in_contact:
                contact[-1] += char
            else:
                in_location = True 
                location += [char]

            in_symmetry = False
            in_handshape = False
            in_orientation = False
            in_repetition = False
            in_special_repetition = False
            in_hand_internal = False
            # leave in_contact on 
            # leave in_brush on
            # leave in_fusion on
            # leave in_simultaneous on
            # leave in_movement on

        elif char in location_diacritic:
            location[-1] += char
        
        # characters unique to contact
        elif char in contact_base:
            
            # add contact to brush symbol if present
            if in_brush: 
                in_contact = True
                contact[-1] += char
                in_brush = False

            # more detailed transcription for initial position
            elif text[i-1] == close_bracket:
                in_initial = True
                initial_position += [char]
            elif in_initial: # end of contact, location, contact sequence
                initial_position[-1] += char
                in_initial = False
            else:    
                in_contact = True
                contact += [char]

            in_symmetry = False
            in_handshape = False
            in_orientation = False
            in_location = False
            in_repetition = False
            in_special_repetition = False
            in_hand_internal = False
            # leave in_fusion on
            # leave in_simultaneous on
            # leave in_movement on
                
        # characters unique to movement
        elif char in movement_base:
            
            if in_movement:
                if in_simultaneous:
                    movement[-1] += char
                elif in_fusion:
                    movement[-1] += char
                elif in_special_repetition:
                    movement[-1] += char
                else:
                    movement += [char]

            # for repeated movements
            elif text[i-1] in repetition:
                in_movement = True
                movement[-1] += char
                
            # beginning of simple movement
            else:
                in_movement = True
                movement += [char] 
                
            in_symmetry = False
            in_handshape = False
            in_orientation = False
            in_brush = False
            in_contact = False
            in_location = False
            in_initial = False
            in_hand_internal = False

        elif char in movement_diacritic:
            if in_repetition:
                repeat[-1] += char
            else:
                movement[-1] += char
                
        # keep fused movements together and parse at end
        elif char == open_fuse:
            movement += [char]
            in_movement = True
            in_fusion = True
            
            in_symmetry = False
            in_handshape = False
            in_orientation = False
            in_brush = False
            in_contact = False
            in_location = False
            in_initial = False
            in_repetition = False
            in_special_repetition = False
            in_simultaneous = False
            in_hand_internal = False
            
        elif char == close_fuse:
            if in_fusion:
                movement[-1] += char

                in_fusion = False
                in_handshape = False # these sometimes occur in movement segment
                in_orientation = False # these sometimes occur in movement segment

            else:
                movement_meta += char # unparsed
                in_fusion = False
        
        elif char in repetition:
            # special type of repetition relating two movements
            if in_special_repetition:
                movement[-1] += char
            # multiple normal repetition
            elif in_repetition:
                repeat[-1] += char
            # normal repetition
            else:
                in_repetition = True
                repeat += [char]
        
        # some diacritics can occur in most environments
        elif char in ambiguous_diacritic: 
            if in_symmetry:
                symmetry[-1] += char
            elif in_handshape:
                handshape[-1] += char
            elif in_orientation:
                orientation[-1] += char
            elif in_contact:
                contact[-1] += char
            elif in_location:
                location[-1] += char
            elif in_movement: 
                if char in ambiguous_location: # can appear in movement segment
                    if in_hand_internal:
                        movement[-1] += char
                    elif text[i-1] == hand_internal_mov:
                        in_hand_internal = True
                        movement[-1] += char
                    else:
                        in_location = True
                        location += [char]
                else:
                    movement[-1] += char
            # must be location
            else:
                in_location = True
                location += [char] 
            
        # check the next character after open bracket
        elif char == open_bracket: 
            if text[i+1] in ambiguous_diacritic: # I think this must be location                
                location_meta += char
            elif text[i+1] in handshape_base:
                handshapes_meta += char                
            elif text[i+1] in orientation_base: # seems unlikely
                orientation_meta += char                
            elif text[i+1] in contact_base: # seems unlikely
                location_meta += char            
            elif text[i+1] in location_base:
                location_meta += char                
            elif text[i+1] in movement_base:
                # three options: (a) no dominance symbol, thus simultaneous
                if dominance_meta not in text[i:]: # this may be a problem for compounds
                    in_simultaneous = True
                    in_movement = True
                    movement += [char]
                # (b) simultaneous and dominance symbol
                elif dominance_meta in text[i:]: # this may be a problem for compounds
                    if text[i-1] == open_bracket:
                        in_simultaneous = True
                        in_movement = True
                        movement += [char]
                    else:
                        movement_meta += char
                # or (c) nondominant, no simultaneity
                else:
                    movement_meta += char
            elif text[i+1] == open_fuse:
                movement_meta += char
            elif text[i+1] == open_bracket: # two open brackets, the second is movement
                movement_meta += char
                
            # grouping symbol; I think this must be movement
            elif text[i+1] == open_par: 
                movement_meta += char
            else:
                rest += char # unparsed

        # check the next character after open paragraph
        elif char == open_par: 
            if text[i+1] in ambiguous_diacritic: # I think this must be location                
                location_meta += char
            elif text[i+1] == handshape_base: # rare
                handshapes_meta += char
            elif text[i+1] == orientation_base: # rare
                orientation_meta += char        
            elif text[i+1] == brush:
                contact_meta += char
            elif text[i+1] in contact_base:
                contact_meta += char            
            elif text[i+1] in location_base:
                # for locations below the waist; turn on location environment
                if text[i-1] in location_base:
                    in_location = True
                    location_meta += char
                else:
                    location_meta += char                
            elif text[i+1] in movement_base:
                in_grouped_movement = True # to do: for groups of movement symbols
                movement_meta += char
            elif text[i+1] in repetition:
                in_movement = True
                in_special_repetition = True
                movement[-1] += char
            else:
                rest += char # unparsed characters
        
        # marker for 2-handed sign
        elif char == dominance_meta: 
            if in_handshape:
                # handshape change in movement environment
                if dominance_meta not in handshapes_meta:
                    handshapes_meta += char
                else:
                    movement_meta += char
            elif in_orientation:
                # orientation change in movement environment
                if dominance_meta not in orientation_meta:
                    orientation_meta += char
                else:
                    movement_meta += char
            elif in_contact:
                # may occur in movement environment
                if dominance_meta not in location_meta:
                    location_meta += char
                else:
                    movement_meta += char
            elif in_location:
                # may occur in movement environment
                if dominance_meta not in location_meta:
                    location_meta += char
                else:
                    movement_meta += char
            elif in_movement:
                movement_meta += char
            else:
                rest += char
            
            # turn everything off, so next symbol starts new segment
            in_symmetry = False
            in_handshape = False
            in_orientation = False
            in_contact = False
            in_brush = False
            in_location = False
            in_initial = False
            in_movement = False
            in_simultaneous = False
            in_fusion = False
            in_repetition = False
            in_special_repetition = False
                
        # assign close brackets
        elif char == close_bracket:
            # close simlutaneous movement if open bracket in movement
            if in_simultaneous:
                movement[-1] += char
                in_movement = True # leave on to parse dominance_meta in 2-handed signs, with simultaneous
                
                in_handshape = False
                in_orientation = False
                in_contact = False
                in_location = False
                in_simultaneous = False
                                        
            elif in_handshape:
                handshapes_meta += char
                in_handshape = False
                
            elif in_orientation:
                orientation_meta += char
                in_orientation = False
                
            elif in_location:
                location_meta += char
                in_location = False
                
            elif in_contact:
                location_meta += char
                in_location = False

            elif in_movement:
                movement_meta += char
                in_movement= False
                
            else:
                rest += char # unparsed
                
        # assign close paragaph
        elif char == close_par:
            if in_grouped_movement: # to do
                movement_meta += char
            elif in_contact:
                contact_meta += char
            elif in_handshape:
                handshapes_meta += char
            elif in_orientation:
                orientation_meta += char
            elif in_location:
                location_meta += char
            elif in_movement:
                if in_special_repetition:
                    movement[-1] += char
                else:
                    movement_meta += char
            else:
                rest += char # unparsed
                
    # handshapes
    if h:
        # determine dominant hand, no symmetry
        if dominance_meta in handshapes_meta:
            # first in list is dominant
            dominant_hand = handshape.pop(0)
            # second in list is nondominant
            nondominant_hand = handshape.pop(0)
            # all others
            if len(handshape) > 0:
                if len (handshape) > 1:
                    handshape_change = handshape
                else:
                    handshape_change = ''.join(handshape)
            else:
                handshape_change = ''
        # one hand, no symmetry
        else:
            # first in list is dominant
            dominant_hand = handshape.pop(0)
            # none
            nondominant_hand = ''
            # all others
            if len(handshape) > 0:
                if len(handshape) > 1:
                    handshape_change = handshape
                else:
                    handshape_change = ''.join(handshape)
            else:
                handshape_change = ''
    else:
        dominant_hand = ''
        nondominant_hand = ''
        handshape_change = ''
    
    # orientation
    if o:
    # determine dominant orientation
        if dominance_meta in orientation_meta:
            dominant_orientation = orientation.pop(0)
            nondominant_orientation = orientation.pop(0)
            if len(orientation) > 0:
                if len(orientation) > 1:
                    orientation_change = orientation
                else:
                    orientation_change = ''.join(orientation)
            else:
                orientation_change = ''
        # only one hand
        else:
            dominant_orientation = orientation.pop(0)
            nondominant_orientation = ''
            if len(orientation) > 0:
                if len(orientation) > 1:
                    orientation_change = orientation
                else:
                    orientation_change = ''.join(orientation)
            else:
                orientation_change = ''
    else:
        dominant_orientation = ''
        orientation_change = ''
        nondominant_orientation = ''

    # location
    if l:
        # check if normal or detailed transcription style
        if initial_position != []:
            dominant_location = location.pop(0)
            nondominant_location = location.pop(0)
            if len(location) > 0:
                if len(location) > 1:
                    location_change = location
                else:
                    location_change = ''.join(location)
            else:
                location_change = ''
            
        # determine dominant location
        elif dominance_meta in location_meta:
            dominant_location = location.pop(0)
            nondominant_location = location.pop(0)
            if len(location) > 0:
                if len(location) > 1:
                    location_change = location
                else:
                    location_change = ''.join(location)
            else:
                location_change = ''
            
        # only one hand
        else:
            dominant_location = location.pop(0)
            nondominant_location = ''
            if len(location) > 0:
                if len(location) > 1:
                    location_change = location
                else:
                    location_change = ''.join(location)
            else:
                location_change = ''
    else:
        dominant_location = ''
        location_change = ''
        nondominant_location = ''
        initial_position = ''
   
    # determine dominant contact: unsure if nondominant contact is possible transcription
    # may not occur in some signs
    if len(contact) > 0:
        if dominance_meta in location_meta:
            dominant_contact = contact.pop(0)
            if len(contact) > 0:
                if len(contact) > 1:
                    contact_change = contact
                else:
                    contact_change = ''.join(contact)
            else:
                contact_change = ''
    
        # only one hand
        else:
            dominant_contact = contact.pop(0)
            if len(contact) > 0:
                if len(contact) > 1:
                    contact_change = contact
                else:
                    contact_change = ''.join(contact)
            else:
                contact_change = ''
    else:
        dominant_contact = ''
        contact_change = ''

    # movement
    if m:
        # parse contents of simultaneous, fused, and special-repetition movements
        movement_updated = []
        for item in movement:
            if open_bracket in item and close_bracket in item:
                simul_mov = []
                stripped_movement = item.strip('')
                for i, char in enumerate(stripped_movement):
                    if char in movement_base:
                        simul_mov += [char]
                    elif char in movement_diacritic:
                        simul_mov[-1] += char
                    elif char in ambiguous_location: # finger internal movement
                        simul_mov[-1] += char
                simul_mov.append('simultaneous')
                movement_updated.append(simul_mov)
            elif open_fuse in item and close_fuse in item: 
                fused_mov = []
                stripped_movement = item.strip('')
                for i, char in enumerate(stripped_movement):
                    if char in movement_base:
                        fused_mov += [char]
                    elif char in movement_diacritic:
                        fused_mov[-1] += char
                    elif char in ambiguous_location: # finger internal movement
                        fused_mov[-1] += char
                fused_mov.append('fused')
                movement_updated.append(fused_mov)
            elif open_par in item and close_par in item:
                repeated_mov = []
                repeating = ''
                stripped_movement = item.replace('', '').replace('', '')
                for i, char in enumerate(stripped_movement):
                    if char in movement_base:
                        repeated_mov += [char]
                    elif char in movement_diacritic:
                        repeated_mov[-1] += char
                    elif char in ambiguous_location: # finger internal movement
                        repeated_mov[-1] += char
                    elif char in repetition:
                        repeating += char
                repeated_mov.append(repeating)
                movement_updated.append(repeated_mov)
            else:
                movement_updated.append(item)
        
        # determine dominant movement
        if dominance_meta in movement_meta:
            dominant_movement = movement_updated.pop(0)
            nondominant_movement = movement_updated.pop(0)
            if len(movement_updated) > 0:
                if len(movement_updated) > 1:
                    movement_change = movement_updated
                else:
                    movement_change = ''.join(movement_updated)
            else:
                movement_change = ''
        # only one hand
        else:
            dominant_movement = movement_updated.pop(0)
            nondominant_movement = ''
            if len(movement_updated) > 0:
                if type(movement_updated) == list:
                    movement_change = movement_updated
                else:
                    movement_change = ''.join(movement_updated)
            else:
                movement_change = ''
                
    else:
        dominant_movement = ''
        nondominant_movement = ''
        movement_change = ''
    
    # repetition symbols
    if repeat != []:
        if len(repeat) > 1:
            repeat = repeat
        else:
            repeat = repeat.pop(0)
    else:
        repeat = ''
    
    data = {
            'symmetry': symmetry,
            'initial position': initial_position,
            'dominant': {
                'shape': [dominant_hand, handshape_change],
                'orientation': [dominant_orientation, orientation_change],
                'location': [dominant_location, location_change],
                'contact': [dominant_contact, contact_change],
                'movement': [dominant_movement, movement_change],
                'repetition': [repeat],
                'is_dominant': True
                },
            'nondominant': {
                'shape': [nondominant_hand, ''],
                'orientation': [nondominant_orientation, ''],
                'location': [nondominant_location, ''],
                'contact': [],
                'movement': [nondominant_movement, ''],
                'is_dominant': False
                },
            # can be removed later, but keep now to check parsing
            'meta': {
                'handshape': handshapes_meta,
                'orientation': orientation_meta,
                'contact': contact_meta,
                'location': location_meta,
                'movement': movement_meta,
                'rest': rest
                }
            }
    return data

@attr.s
class Hand(object):
    shape = attr.ib(default='')
    orientation = attr.ib(default='')
    location = attr.ib(default='')
    movement = attr.ib(default='')
    is_dominant = attr.ib(default='')
    contact = attr.ib(default='')
    repetition = attr.ib(default='')

    
    def distance(self, other, weights=None, compare=None):
        """
        Compare one hand with another when comparing a sign.
        
        Notes
        -----
        `weights` is a dictionary with the characteristics one wants to compare
        and a weight assigned to it. `compare` is a function that yields a
        score between one and zero when comparing strings. The default is a
        very simple function that simply yields 1 in case of difference, and 0
        in case of identity.
        """
        weights = weights or {
                'shape': 5,
                'orientation': 3,
                'location': 2,
                'movement': 1,
                'contact': 2,
                'repetition': 2
                }
        
        def identity(string1, string2):
            if string1 == string2:
                return 0
            return 1

        compare = compare or identity

        # get all values, so we divide by them when weighting
        weight_sum = sum(weights.values())
        # we make an array with the scores
        scores = []

        for attribute, weight in sorted(weights.items()):
            attr1, attr2 = getattr(self, attribute), getattr(other, attribute)
            scores += [compare(attr1, attr2)*weight]
        return sum(scores)/weight_sum
    

@attr.s
class Sign(object):
    text = attr.ib(default='')
    dominant = attr.ib(default='')
    nondominant = attr.ib(default='')
    meta = attr.ib(default={'handshape': '', 'orientation': '',
        'location': '', 'movement': '', 'rest': ''})
    
    @classmethod
    def from_text(cls, text):
        data = parse_hamnosys(text)
        dominant = Hand(**data['dominant'])
        nondominant = Hand(**data['nondominant'])
        meta = data['meta']
        return cls(
                text=text, 
                dominant=dominant, 
                nondominant=nondominant, 
                meta=meta
                )

    def pprint(self, as_ascii=True):
        if not as_ascii:
            modify = lambda x: x
        else:
            modify = ascify
        table = [['Category', 'Dominant', 'Change', 'Nondominant']]
        for category in ['shape', 'orientation', 'location', 'movement']:
            table += [[
                category, 
                modify(getattr(self.dominant, category)[0]),
                modify(getattr(self.dominant, category)[1]),
                modify(getattr(self.nondominant, category)[0])
                    ]]
        print(self.text)
        print(tabulate(table, headers='firstrow', tablefmt='pipe'))





# old data, to be deleted
#        data = {
#                'symmetry': symmetry,
#                'handshape': {
#                    'dominant': {
#                        'shape': dominant_hand,
#                        'change': handshape_change
#                        },
#                    'nondominant': {
#                        'shape': nondominant_hand,
#                        'change': '' # is this never annotated?
#                        },
#                    },
#                'orientation': { 
#                    'dominant': {
#                        'orientation': dominant_orientation,
#                        'change': orientation_change
#                        },
#                    'nondominant': {
#                        'orientation': nondominant_orientation,
#                        'change': '' # is this never annotated?
#                        },
#                    },
#                'contact': contact,
#                'location': { 
#                    'dominant': {
#                        'location': dominant_location,
#                        'change': location_change
#                        },
#                    'nondominant': {
#                        'location': nondominant_location
#                        },
#                    },
#                'movement': { 
#                    'dominant': {
#                        'movement': dominant_movement,
#                        'change': movement_change
#                        },
#                    'nondominant': {
#                        'movement': nondominant_movement
#                        },
#                    },                
##                'errors': unparsable,
#                'handshape metasymbols': handshapes_meta,
#                'orientation metasymbols': orientation_meta,
#                'location metasymbols': location_meta,
#                'movement metasymbols': movement_meta,
#                'rest': rest
#               }
#    else:
#        data = {
#                'symmetry': ascify(symmetry),
#                'handshape': {
#                    'dominant': {
#                        'shape': ascify(dominant_hand),
#                        'change': ascify(handshape_change)
#                        },
#                    'nondominant': {
#                        'shape': ascify(nondominant_hand),
#                        'change': '' # is this never annotated?
#                        },
#                    },
#                'orientation': {
#                    'dominant': {
#                        'orientation': ascify(dominant_orientation),
#                        'change': ascify(orientation_change)
#                        },
#                    'nondominant': {
#                        'orientation': ascify(nondominant_orientation),
#                        'change': '' # is this never annotated?
#                        },
#                    },
#                'contact': ascify(contact),
#                'location': { 
#                    'dominant': {
#                        'location': ascify(dominant_location),
#                        'change': ascify(location_change)
#                        },
#                    'nondominant': {
#                        'location': ascify(nondominant_location)
#                        },
#                    },                
#                'movement': { 
#                    'dominant': {
#                        'movement': ascify(dominant_movement),
#                        'change': ascify(movement_change)
#                        },
#                    'nondominant': {
#                        'movement': ascify(nondominant_movement)
#                        },
#                    },                
##                'errors': ascify(unparsable),
#                'handshape_metasymbols': ascify(handshapes_meta),
#                'orientation_metasymbols': ascify(orientation_meta),
#                'location_metasymbols': ascify(location_meta),
#                'movement_metasymbols': ascify(movement_meta),
#                'rest': ascify(rest)
#                }

