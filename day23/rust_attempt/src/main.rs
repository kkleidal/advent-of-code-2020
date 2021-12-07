use std::cmp::max;
use std::collections::HashMap;
use std::io;

#[derive(Debug)]
struct CupCollection {
    cups: Vec<Cup>,
    cup_lookup: HashMap<u64, usize>, // map label to index
    current_cup: usize,              // index
}

#[derive(Debug)]
struct Cup {
    label: u64,
    next: usize,
}

impl CupCollection {
    fn parse(initial_state: &str, size: usize) -> CupCollection {
        let mut cups: Vec<Cup> = Vec::new();
        let mut cup_lookup: HashMap<u64, usize> = HashMap::new();
        let n = max(size, initial_state.len());
        for (i, c) in initial_state.chars().enumerate() {
            let cstr: String = vec![c].iter().collect();
            let x: u64 = cstr.parse().expect("Invalid integer");
            let cup = Cup {
                label: x,
                next: (i + 1) % n,
            };
            cups.push(cup);
            cup_lookup.insert(x, i);
        }
        for i in initial_state.len()..n {
            let x: u64 = (i + 1).try_into().expect("Invalid cast");
            let cup = Cup {
                label: x,
                next: (i + 1) % n,
            };
            cup_lookup.insert(x, i);
            cups.push(cup);
        }
        CupCollection {
            cups,
            cup_lookup,
            current_cup: 0,
        }
    }

    fn normalize(&self) -> u64 {
        let mut out: u64 = 0;
        let start: u64 = 1;
        let one_ptr = *self.cup_lookup.get(&start).expect("Missing");
        let mut ptr = self.cups[one_ptr].next;
        while ptr != one_ptr {
            out = out * 10 + self.cups[ptr].label;
            ptr = self.cups[ptr].next;
        }
        out
    }

    fn iteration(&mut self) {
        let current_ptr = self.current_cup;
        let current = self.cups[current_ptr].label;

        let picked1_ptr = self.cups[current_ptr].next;
        let picked2_ptr = self.cups[picked1_ptr].next;
        let picked3_ptr = self.cups[picked2_ptr].next;

        let picked1 = self.cups[picked1_ptr].label;
        let picked2 = self.cups[picked2_ptr].label;
        let picked3 = self.cups[picked3_ptr].label;

        let after_ptr = self.cups[picked3_ptr].next;
        self.cups[current_ptr].next = after_ptr;

        let dest = {
            let mut out = current;
            let n: u64 = self.cups.len().try_into().expect("Can't cast");
            while out == current || out == picked1 || out == picked2 || out == picked3 {
                out = if out == 1 { n } else { out - 1 }
            }
            out
        };

        let dest_ptr = *self.cup_lookup.get(&dest).expect("Missing");
        let after_dest_ptr = self.cups[dest_ptr].next;

        self.cups[dest_ptr].next = picked1_ptr;

        self.cups[picked3_ptr].next = after_dest_ptr;

        self.current_cup = after_ptr;
    }

    fn part2(&self) -> u64 {
        let start: u64 = 1;
        let one_ptr = self.cup_lookup[&start];
        let next1_ptr = self.cups[one_ptr].next;
        let next2_ptr = self.cups[next1_ptr].next;
        self.cups[next1_ptr].label * self.cups[next2_ptr].label
    }
}

fn main() {
    let mut buf = String::new();
    let n = io::stdin()
        .read_line(&mut buf)
        .expect("Failed to read stdin");
    assert!(n > 0);

    let initial_state_str = buf.trim();

    let mut collection = CupCollection::parse(initial_state_str, 0);
    for _ in 0..100 {
        collection.iteration();
    }
    println!("Part 1: {:?}", collection.normalize());

    let n_cups = 1000000;
    let n_iter = 10000000;
    let mut collection = CupCollection::parse(initial_state_str, n_cups);

    for _ in 0..n_iter {
        collection.iteration();
    }
    println!("Part 2: {:?}", collection.part2());
}
