| line localSeat seatIds maxSeatID |
seatIds := OrderedCollection new.
[(line := stdin nextLine) notNil] whileTrue: [
    localSeat := 0.
    line asArray do: [:ch |
        ((ch == $B) or: [ch == $R]) ifTrue: [
          localSeat := localSeat bitOr: 1
        ].
        localSeat := localSeat bitShift: 1.
    ].
    localSeat := localSeat bitShift: -1.
    seatIds add: localSeat.
].

" Print all the seat IDs "
" seatIds do: [:seatId |
    Transcript show: seatId asString; cr.
]."

" Find the max "
maxSeatID := seatIds inject: 0 into: [:a :b | (a > b) ifTrue: [a] ifFalse: [b]].
Transcript show: maxSeatID asString; cr.
