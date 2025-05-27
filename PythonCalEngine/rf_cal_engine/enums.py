from enum import Enum

class StandardType(Enum):
    Unknown = 0
    """
    For single-ended and dual probe.
    """
    Ceramic = 1
    """
    For single-ended and dual probe.
    """
    Air = 2
    """
    For single-ended and dual probe.
    """
    Open = 3
    """
    For single-ended and dual probe.
    """
    Short = 4
    """
    For single-ended and dual probe.
    """
    Load = 5
    """
    For single-ended and dual probe.
    """
    Thru = 6
    """
    For single-ended probe.
    """
    ThruStraight = 7
    """
    For dual probe.
    1   3
    2   4
    Port13 and Port24    
    """
    
    ThruLoopBackLeft = 8
    """
    For dual probe.
    1   3
    2   4
    Port12
    """
    ThruLoopBackRight = 9
    """
    For dual probe.
    1   3
    2   4
    Port34
    """
    ThruLoopBack = 10
    """
    For dual probe.
    1   3
    2   4
    Port12 and Port34
    """
    ThruNwSe = 11
    """
    For dual probe.
    1   3
    2   4
    Port14
    """
    ThruSwNe = 12
    """
    For dual probe.
    1   3
    2   4
    Port23
    """
    Line1 = 13
    """
    For single-ended and dual probe.
    """
    Line2 = 14
    """
    For single-ended and dual probe.
    """
    Line3 = 15
    """
    For single-ended and dual probe.
    """
    Line4 = 16
    """
    For single-ended and dual probe.
    """
    Line5 = 17
    """
    For single-ended and dual probe.
    """
    Line6 = 18
    """
    For single-ended and dual probe.
    """
    Line7 = 19
    """
    For single-ended and dual probe.
    """
    Line8 = 20
    """
    For single-ended and dual probe.
    """
    Line9 = 21
    """
    For single-ended and dual probe.
    """
    Line10 = 22
    """
    For single-ended and dual probe.
    """
    Line11 = 23
    """
    For single-ended and dual probe.
    """
    Line12 = 24
    """
    For single-ended and dual probe.
    """
    Line13 = 25
    """
    For single-ended and dual probe.
    """
    Line14 = 26
    """
    For single-ended and dual probe.
    """
    Line15 = 27
    """
    For single-ended and dual probe.
    """
    Line16 = 28
    """
    For single-ended and dual probe.
    """
    Line17 = 29
    """
    For single-ended and dual probe.
    """
    Line18 = 30
    """
    For single-ended and dual probe.
    """
    Line19 = 31
    """
    For single-ended and dual probe.
    """
    Line20 = 32
    """
    For single-ended and dual probe.
    """
    Align= 33
    """
    For probe alignment.
    """
    Ruler= 34
    """
    For measuring distance between probes.
    """


class StandardThruType(Enum):
    Unknown = 0
    Thru = StandardType.Thru

class EErrorTerms12(Enum):
    Unknown = 0
    """
    Unknown error term
    """
    FwdEd = 1
    """
    Forward Directivity
    """
    FwdEs = 2
    """
    Forward Source Match
    """
    FwdErt = 3
    """
    Forward Reflection Tracking
    """
    RevEd = 4
    """
    Reverse Directivity
    """
    RevEs = 5
    """
    Reverse Source Match
    """
    RevErt = 6
    """
    Reverse Reflection Tracking
    """
    FwdEx = 7
    """
    Forward Isolation
    """
    FwdEl = 8
    """
    Forward Load Match
    """
    FwdEtt = 9
    """
    Forward Transmission Tracking
    """
    RevEx = 10
    """
    Reverse Isolation
    """
    RevEl = 11
    """
    Reverse Load Match
    """
    RevEtt = 12
    """
    Reverse Transmission Tracking
    """
