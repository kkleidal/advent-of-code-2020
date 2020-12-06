
Object subclass: AOCDay5Part1 [
  | mask count |

  AOCDay5Part1 class >> new [
      | r |
      r := super new.
      ^ r init.
  ]

  init [
    FileStream fileIn: '../utils.st'.
    count := 0.
    mask := Array new: 26.
    self clearMask.
  ]

  clearMask [
    mask := mask collect: [:a | false].
  ]


  endOfGroup [
    " Sum up the current mask and clear it (end of ticket) "
    | intMask localCount |
    intMask := mask collect: [:a | a asInteger].
    localCount := intMask sum.
    count := count + localCount.
    self clearMask.
  ]

  solveProblem [
    |line index|
    stdin doTrimmedLines: [ :line |
        ((line size) == 0) ifTrue: [
          self endOfGroup.
        ] ifFalse: [
          line asArray do: [:ch |
              index := (ch asciiValue) - ($a asciiValue) + 1.
              mask at: index put: true.
          ].
        ]
    ].
    self endOfGroup.
    ^count.
  ]
]

|problem|
problem := AOCDay5Part1 new. 
Transcript show: (problem solveProblem) asString; cr.
