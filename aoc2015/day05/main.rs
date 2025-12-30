use std::collections::HashMap;

fn parse(filename: &str) -> String {
    std::fs::read_to_string(filename).expect("Provide input to run")
}

fn is_nice(line: &str) -> bool {
    let mut still_nice = false;
    let mut num_vowels = 0;
    for (i, ch) in line.chars().enumerate() {
        if i < (line.len() - 1) {
            let ch2 = line.chars().nth(i + 1).unwrap();
            if ch == ch2 {
                still_nice = true;
            }
            if (ch == 'a' && ch2 == 'b')
                || (ch == 'c' && ch2 == 'd')
                || (ch == 'p' && ch2 == 'q')
                || (ch == 'x' && ch2 == 'y')
            {
                return false;
            }
        }
        if ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u' {
            num_vowels += 1;
        }
    }
    still_nice && (num_vowels >= 3)
}

fn task1(content: &str) -> i64 {
    let mut result = 0;
    for line in content.lines() {
        if is_nice(line) {
            result += 1;
        }
    }
    result
}

fn is_nice2(line: &str) -> bool {
    let mut first_condition = false;
    let mut combinations = HashMap::new();
    for (i, tp) in line.chars().zip(line.chars().skip(1)).enumerate() {
        if *combinations.get(&tp).unwrap_or(&i) + 1 < i {
            first_condition = true;
            break;
        }
        if !combinations.contains_key(&tp) {
            combinations.insert(tp, i);
        }
    }
    if !first_condition {
        return false;
    }
    for (ch1, ch2) in line.chars().zip(line.chars().skip(2)) {
        if ch1 == ch2 {
            return true;
        }
    }
    false
}

fn task2(content: &str) -> usize {
    let mut result = 0;
    for line in content.lines() {
        if is_nice2(line) {
            result += 1;
        }
    }
    result
}

fn main() {
    let content = parse("day05/input");

    let res1 = task1(&content);
    println!("Result 1: {}", res1);

    let res2 = task2(&content);
    println!("Result 2: {}", res2);
}
