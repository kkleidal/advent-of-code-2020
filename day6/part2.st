Collection extend [
  intersect: other [
    | outVal otherValue |
    " Intersect two boolean arrays "
    outVal := Array new: (self size).
    self doWithIndex: [:value :i |
      otherValue := other at: i.
      outVal at: i put: (value & otherValue).
    ].
    ^outVal.
  ]

  union: other [
    | outVal otherValue |
    " Union two boolean arrays "
    outVal := Array new: (self size).
    self doWithIndex: [:value :i |
      otherValue := other at: i.
      outVal at: i put: (value | otherValue).
    ].
    ^outVal.
  ]

  not [
    " Invert boolean array "
    ^self collect: [:x | x not].
  ]
]


Object subclass: AOCDay5Part2 [
  | anyUsedMask allUsedMask count |

  AOCDay5Part2 class >> new [
      | r |
      r := super new.
      ^ r init.
  ]

  init [
    FileStream fileIn: '../utils.st'.
    count := 0.
    self clearMask.
  ]

  makeMask: fill [
    | mask |
    mask := Array new: 26.
    mask := mask collect: [:a | fill].
    ^mask.
  ]

  clearMask [
    anyUsedMask := self makeMask: false.
    allUsedMask := self makeMask: true.
  ]


  endOfGroup [
    " Sum up the current mask and clear it (end of ticket) "
    | mask intMask localCount |
    mask := anyUsedMask intersect: allUsedMask.
    intMask := mask collect: [:a | a asInteger].
    localCount := intMask sum.
    count := count + localCount.
    self clearMask.
  ]

  solveProblem [
    |line index localMask|
    " Loop over the input and compute the masks for each person, group, and the 
      sum across groups.
    "
    stdin doTrimmedLines: [ :line |
        ((line size) == 0) ifTrue: [
          self endOfGroup.
        ] ifFalse: [
          localMask := self makeMask: false.
          line asArray do: [:ch |
              index := (ch asciiValue) - ($a asciiValue) + 1.
              localMask at: index put: true.
          ].
          anyUsedMask := anyUsedMask union: localMask.
          allUsedMask := allUsedMask intersect: localMask.
        ]
    ].
    self endOfGroup.
    ^count.
  ]
]

|problem|
problem := AOCDay5Part2 new. 
Transcript show: (problem solveProblem) asString; cr.
