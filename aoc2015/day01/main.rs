fn parse(filename: &str) -> String {
    std::fs::read_to_string(filename).expect("Provide input to run")
}

fn task1(content: &str) -> i64 {
    let mut result = 0;
    for element in content.chars() {
        result += if element == '(' { 1 } else { -1 };
    }
    result
}

fn task2(content: &str) -> usize {
    let mut level = 0;
    for (idx, element) in content.chars().enumerate() {
        level += if element == '(' { 1 } else { -1 };
        if level == -1 {
            return idx + 1;
        }
    }
    0
}

fn main() {
    let content = parse("day01/input");

    let res1 = task1(&content);
    println!("Result 1: {}", res1);

    let res2 = task2(&content);
    println!("Result 2: {}", res2);
}
