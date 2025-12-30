use std::collections::HashSet;

fn parse(filename: &str) -> String {
    std::fs::read_to_string(filename).expect("Provide input to run")
}

fn task1(content: &str) -> usize {
    let mut positions = HashSet::new();
    let mut position = (0, 0);
    positions.insert(position);
    for char in content.chars() {
        match char {
            '>' => {
                position.0 += 1;
            }
            '<' => {
                position.0 -= 1;
            }
            '^' => {
                position.1 += 1;
            }
            'v' => {
                position.1 -= 1;
            }
            _ => {
                panic!("Invalid movement {}", char);
            }
        };
        positions.insert(position);
    }
    positions.len()
}

fn task2(content: &str) -> usize {
    let mut positions = HashSet::new();
    let mut position: [(i64, i64); 2] = [(0, 0), (0, 0)];
    positions.insert(position[0]);
    for (i, char) in content.chars().enumerate() {
        match char {
            '>' => {
                position[i % 2].0 += 1;
            }
            '<' => {
                position[i % 2].0 -= 1;
            }
            '^' => {
                position[i % 2].1 += 1;
            }
            'v' => {
                position[i % 2].1 -= 1;
            }
            _ => {
                panic!("Invalid movement {}", char);
            }
        };
        positions.insert(position[i % 2]);
    }

    positions.len()
}

fn main() {
    let content = parse("day03/input");

    let res1 = task1(&content);
    println!("Result 1: {}", res1);
    // 2080 too low

    let res2 = task2(&content);
    println!("Result 2: {}", res2);
}
