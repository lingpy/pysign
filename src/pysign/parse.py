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
    brush=""
    location_base=""
    location_diacritic=""
    contact_base=""
    movement_base=""
    movement_diacritic=""
    repetition=""
    ambiguous_diacritic=""
    open_bracket=""
    open_par=""
    close_par=""
    dominance_meta=""
    close_bracket=""

    # set up environments and variables
    in_symmetry, symmetry = False, []
    in_handshape, handshape, handshapes_meta = False, [], []
    in_brush = False
    in_contact, contact, contact_meta = False, [], []
    in_location, location, location_meta = False, [], []
    in_initial, initial_position = False, []
    in_orientation, orientation, orientation_meta = False, [], []
    in_movement, movement, movement_meta = False, [], []
    in_repetition, repeat = False, []
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
            in_repetition = False
            rest += char # not strictly necessary
        
        # characters unique to symmetry
        elif char in symmetry_base:
            # turn on symmetry environment
            in_symmetry = True 
            symmetry += [char]
            
        # characters unique to handshape
        elif char in handshape_base:
            # turn off other environments
            in_symmetry = False 
            in_orientation = False
            in_contact = False
            in_brush = False
            in_location = False
            in_initial = False
            in_movement = False 
            in_repetition = False
            # turn on handshape environment
            in_handshape = True            
            handshape += [char]
        elif char in handshape_diacritic:
            handshape[-1] += char
        
        # characters unique to orientation
        elif char in orientation_base:
            in_symmetry = False
            in_handshape = False
            in_contact = False
            in_brush = False
            in_location = False
            in_initial = False
            in_movement = False
            in_repetition = False
            # can have two base characters in sequence
            if in_orientation:
                orientation[-1] += char
            else:
                in_orientation = True 
                orientation += [char]
        elif char == orientation_diacritic: 
            orientation[-1] += char

        # brush and contact symbols can be separated, but should be joined after parsing
        elif char == brush: 
            in_symmetry = False
            in_handshape = False
            in_orientation = False
            in_contact = False
            in_location = False
            in_initial = False
            in_movement = False
            in_repetition = False

            in_brush = True
            contact += [char]

        # characters unique to location
        elif char in location_base:
            in_symmetry = False
            in_handshape = False
            in_orientation = False
            in_contact = False 
            # leave in_brush environment on, as location symbol intervenes between brush and contact
            in_movement = False
            in_repetition = False
            # can have two location base characters in sequence
            if in_location:
                location[-1] += char
            # more detailed transcription option for initial position
            elif in_initial:
                initial_position[-1] += char
            else:
                in_location = True 
                location += [char]
        elif char in location_diacritic: 
            location[-1] += char
        
        # characters unique to contact
        elif char in contact_base:
            in_symmetry = False
            in_handshape = False
            in_orientation = False
            in_location = False
            in_movement = False
            in_repetition = False
            
            # add contact to brush symbol if present
            if in_brush: 
                in_brush = False
                in_contact = True
                contact[-1] += char
            # more detailed transcription for initial position
            elif text[i-1] == close_bracket:
                in_initial = True
                initial_position += [char]
            elif in_initial:
                initial_position[-1] += char
            # normal contact type
            else:    
                in_contact = True
                contact += [char]
                
        # characters unique to movement
        elif char in movement_base:
            in_symmetry = False
            in_handshape = False
            in_orientation = False
            in_brush = False
            in_contact = False
            in_location = False
            in_initial = False
            in_repetition = False
            
            # for simultaneous movement
            if in_movement:
                if open_bracket in movement[-1]: # this may throw an error 
                    in_movement = True
                    movement[-1] += char
                # special type relating two movements
                elif text[i-1] in repetition:
                    in_movement = True
                    movement[-1] += char
                # sequential movement
                else:
                    movement += [char]
            # special type relating two movements
            elif text[i-1] in repetition:
                in_movement = True
                movement[-1] += char
            # beginning of simple movement
            else:
                in_movement = True
                movement += [char] 
        elif char in movement_diacritic: 
            movement[-1] += char
        
        # related to movement, but it may be better to parse in a separate category
        elif char in repetition:
            # special type of repetition relating two movements
            if text[i-1] == open_par:
                movement[-1] += char
            elif in_repetition:
                repeat[-1] += char
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
                movement[-1] += char
            # must be location
            else:
                in_location = True
                location += [char] 
            
        # check the next character after open bracket
        elif char == open_bracket: 
            in_symmetry = False
            in_handshape = False
            in_orientation = False
            in_contact = False 
            in_brush = False
            in_location = False
            in_initial = False
            in_movement = False
            in_repetition = False

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
                if dominance_meta not in text[i:]:
                    in_movement = True
                    movement += [char]
                # (b) simultaneous and dominance symbol
                elif dominance_meta in text[i:]:
                    if text[i-1] == open_bracket:
                        in_movement = True
                        movement += [char]
                    else:
                        movement_meta += char
                # or (c) nondominant, no simultaneity
                else:
                    movement_meta += char
            # two open brackets, the second is movement
            elif text[i+1] == open_bracket: 
                movement_meta += char
                
            # grouping symbols in 2-handed signs; check 2 characters ahead
            elif text[i+1] == open_par:
                in_symmetry = False
                in_handshape = False
                in_orientation = False
                in_contact = False 
                # leave in_brush environment on
                in_location = False
                in_initial = False
                in_movement = False
                in_repetition = False

                if text[i+2] in ambiguous_diacritic: # I think this must be location                
                    location_meta += char
                elif text[i+2] in handshape_base: 
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
                    rest += char # unparsed characters
            else:
                rest += char # unparsed characters

        # check the next character after open paragraph
        elif char == open_par: 
            in_symmetry = False
            in_handshape = False
            in_orientation = False
            in_contact = False 
            # leave in_brush environment on
            in_location = False
            in_initial = False
            in_movement = False
            in_repetition = False
            
            # put these in meta category; I'm not sure what else they are useful for
            if text[i+1] in ambiguous_diacritic: # I think this must be location                
                location_meta += char
            elif text[i+1] in handshape_base:
                handshapes_meta += char                
            elif text[i+1] in orientation_base:
                orientation_meta += char
            elif text[i+1] == brush:
                contact_meta += char
            elif text[i+1] in contact_base:
                contact_meta += char            
            elif text[i+1] in location_base:
                location_meta += char                
            elif text[i+1] in movement_base:
                movement_meta += char
            # special movement type
            elif text[i+1] in repetition:
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
                location_meta += char
            elif in_location:
                location_meta += char
            elif in_movement:
                movement_meta += char
            else:
                rest += char # unparsed characters
                
            # turn off environments; this helps with identifying the detailed initial location type
            in_symmetry = False
            in_handshape = False
            in_orientation = False
            in_contact = False
            in_brush = False
            in_location = False
            in_initial = False
            in_movement = False
            in_repetition = False
                
        # assign close brackets
        elif char == close_bracket:
            # close simultaneous movement if open bracket in movement
            if len(movement) > 0:
                if open_bracket in movement[-1]:
                    movement[-1] += char
                elif open_bracket in movement_meta:
                    if close_bracket not in movement_meta:
                        movement_meta += char
                    else:
                        rest += char # unparsed characters
                else:
                    rest += char # unparsed characters
            
            # check each segment type for dominance symbol, and assign close bracket if not already present
            elif dominance_meta in handshapes_meta:
                if close_bracket not in handshapes_meta:
                    handshapes_meta += char
                elif close_bracket not in orientation_meta:
                    orientation_meta += char
                elif close_bracket not in location_meta:
                    location_meta += char
                elif close_bracket not in movement_meta:
                    movement_meta += char
                # multiple open brackets
                elif movement_meta.count(open_bracket) > 1:
                    movement_meta += char
                else:
                    rest += char # unparsed characters
            elif dominance_meta in orientation_meta:
                if close_bracket not in orientation_meta:
                    orientation_meta += char
                elif close_bracket not in location_meta:
                    location_meta += char
                elif close_bracket not in movement_meta:
                    movement_meta += char
                else:
                    rest += char # unparsed characters
            elif dominance_meta in location_meta:
                if close_bracket not in location_meta:
                    location_meta += char
                elif close_bracket not in movement_meta:
                    movement_meta += char
                else:
                    rest += char # unparsed characters
            elif dominance_meta in movement_meta:
                if close_bracket not in movement_meta:
                    movement_meta += char
                # multiple close brackets for movement
                else:
                    movement_meta += char
            else:
                rest += char # unparsed characters
                
        # assign close paragaph
        elif char == close_par:
            # close special movement type with repetitions
            if in_movement:
                movement[-1] += char
            # close any other open paragraphs, if not already present
            elif open_par in handshapes_meta:
                if close_par not in handshapes_meta:
                    handshapes_meta += char
                elif open_par in orientation_meta:
                    if close_par not in orientation_meta:
                        orientation_meta += char
                    elif open_par in contact_meta:
                        if close_par not in contact_meta:
                            contact_meta += char
                        # multiple open paragraphs for contact
                        elif contact_meta.count(open_par) > contact_meta.count(close_par):
                            contact_meta += char
                        elif open_par in location_meta:
                            if close_par not in location_meta:
                                location_meta += char
                            elif open_par in movement_meta:
                                if close_par not in movement_meta:
                                    movement_meta =+ char
                                else:
                                    rest += char # unparsed
                            else:
                                rest += char # unparsed
                        else:
                            rest += char # unparsed
                    else:
                        rest += char # unparsed
                else:
                    rest += char # unparsed
            elif open_par in orientation_meta:
                if close_par not in orientation_meta:
                    orientation_meta += char
                elif open_par in contact_meta:
                    if close_par not in contact_meta:
                        contact_meta += char
                    elif contact_meta.count(open_par) > contact_meta.count(close_par):
                        contact_meta += char
                    elif open_par in location_meta:
                        if close_par not in location_meta:
                            location_meta += char
                        elif open_par in movement_meta:
                            if close_par not in movement_meta:
                                movement_meta =+ char
                            else:
                                rest += char # unparsed
                        else:
                            rest += char # unparsed
                    else:
                        rest += char # unparsed
                else:
                    rest += char # unparsed
            elif open_par in contact_meta:
                if close_par not in contact_meta:
                    contact_meta += char
                elif contact_meta.count(open_par) > contact_meta.count(close_par):
                    contact_meta += char
                elif open_par in location_meta:
                    if close_par not in location_meta:
                        location_meta += char
                    elif open_par in movement_meta:
                        if close_par not in movement_meta:
                            movement_meta =+ char
                        else:
                            rest += char # unparsed
                    else:
                        rest += char # unparsed
                else:
                    rest += char # unparsed
            elif open_par in location_meta:
                if close_par not in location_meta:
                    location_meta += char
                elif open_par in movement_meta:
                    if close_par not in movement_meta:
                        movement_meta =+ char
                    else:
                        rest += char # unparsed
                else:
                    rest += char # unparsed
            elif open_par in movement_meta:
                if close_par not in movement_meta:
                    movement_meta =+ char
                else:
                    rest += char # unparsed
            else:
                rest += char # unparsed
        else:
            rest += char

    # assign dominant, nondominant, initial location, etc
    
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
                # no upper limit
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
    # determine dominant movement
        if dominance_meta in movement_meta:
            dominant_movement = movement.pop(0)
            nondominant_movement = movement.pop(0)
            if len(movement) > 0:
                if len(movement) > 1:
                    movement_change = movement
                else:
                    movement_change = ''.join(movement)
            else:
                movement_change = ''
        # only one hand
        else:
            dominant_movement = movement.pop(0)
            nondominant_movement = ''
            if len(movement) > 0:
                if len(movement) > 1:
                    movement_change = movement
                else:
                    movement_change = ''.join(movement)
            else:
                movement_change = ''
    else:
        dominant_movement = ''
        dominant_movement = ''
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

