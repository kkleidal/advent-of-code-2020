| line localSeat seatIds maxSeatID seatMask |
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

" Find the max "
maxSeatID := seatIds inject: 0 into: [:a :b | (a > b) ifTrue: [a] ifFalse: [b]].

" Array of all false "
seatMask := Array new: (maxSeatID + 1).
seatMask := seatMask collect: [:a | false].
seatIds do: [:seatId |
    seatMask at: (seatId + 1) put: true.
].
" Find the seat that is empty with two full seats adjacent to it: "
2 to: (maxSeatID - 1) do: [:seatId1 |
    ((((seatMask at: seatId1) not)
        and: [seatMask at: (seatId1 - 1)])
        and: [seatMask at: (seatId1 + 1)]) ifTrue: [
        Transcript show: (seatId1 - 1) asString; cr.
    ].
].
