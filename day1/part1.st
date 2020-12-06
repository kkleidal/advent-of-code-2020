"
import sys

def main():
    input_values = []
    for line in sys.stdin:
        input_values.append(int(line.strip()))

    for i in input_values:
        for j in input_values:
            if i + j == 2020:
                print(i * j)
                return
"



[(line := stdin nextLine) notNil] whileTrue: [
  line := line trimLeft.
  Transcript show: line; cr.
  "
  localSeat := 0.
  line asArray do: [:ch |
      ((ch == $B) or: [ch == $R]) ifTrue: [
        localSeat := localSeat bitOr: 1
      ].
      localSeat := localSeat bitShift: 1.
  ].
  localSeat := localSeat bitShift: -1.
  seatIds add: localSeat.
  "
].
