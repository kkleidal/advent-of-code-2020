String extend
[
   ltrim [
      ^self replacingRegex: '^\s+' with: ''.
   ]
   rtrim [
      ^self replacingRegex: '\s+$' with: ''.
   ]
   trim [
      ^self ltrim rtrim.
   ]
]

Boolean extend [
  asInteger [
    ^self ifTrue: [1] ifFalse: [0].
  ]
]

Collection extend [
  sum [
    ^self inject: 0 into: [:a :b | a + b].
  ]
]

FileStream extend [
  doTrimmedLines: block [
    |line index|
    [(line := stdin nextLine) notNil] whileTrue: [
        line := line trim.
        block value: line.
    ].
  ]
]
