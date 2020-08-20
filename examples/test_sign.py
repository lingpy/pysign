# -*- coding: utf-8 -*-
"""
Transcriptions and targets for the parser
"""

# Example (1) most simple full sign transcription: 
# one dominant hand, one orientation (must have two symbols), one location,
# one movement

{
"   ": # segmented into types
    {
    "symmetry": "",
    "dominant_hand": "", # hamfinger2
    "nondominant_hand": "",
    "handshape_change": "",
    "dominant_orientation": "", # hamextfingeru,hampalmu
    "nondominant_orientation": "",
    "dominant_location": "", # hamchest
    "nondominant_location": "",
    "dominant_movement": "", # hammoveo
    "nondominant_movement": ""
    }
}

# Example (2) most simple two-handed sign with symmetry: 
# one symmetry symbol, one dominant hand, one orientation, one location, 
# one movement

{
"    ":
    {
     "symmetry": "", #hamsymmpar
     "dominant_hand": "", # hamfinger2
     "nondominant_hand": "",
     "handshape_change": "",
     "dominant_orientation": "", # hamextfingeru,hampalmu
     "nondominant_orientation": "",
     "dominant_location": "", # hamchest
     "nondominant_location": "",
     "dominant_movement": "", # hammoveo
     "nondominant_movement": ""
     }
}

# Example (3) two-handed sign completely asymmetrical: 
# one dominant hand, one nondominant hand; orientations, locations,  
# and movements for each hand

{
 "   ":
     {
      "symmetry": "",
      "dominant_hand": "", # hamfinger2
      "nondominant_hand": "", # hamflathand
      "handshape_change": "",
      "dominant_orientation": "", # hamextfingeru,hampalml
      "nondominant_orientation": "", # hamextfingero,hampalmd
      "dominant_location": "", # hamshoulders,hamlrat (sequence matters!)
      "nondominant_location": "", # hamlrat,hamchest (sequence matters!)
      "dominant_movement": "", # hammovedo
      "nondominant_movement": "" # hamnomotion
      }
 }

# Example (4) one-handed sign with handshape change: 
# one dominant hand and handshape change; no orientation provided,
# two locations, and movement as handshape change

{
 "   ":
    {"symmetry": "",
      "dominant_hand": "",
      "nondominant_hand": "",
      "handshape_change": "",
      "dominant_orientation": "",
      "nondominant_orientation": "",
      "dominant_location": ["", ""],# beginning and ending locations
      "nondominant_location": "",
      "dominant_movement": "",
      "nondominant_movement": ""
    }
}
