fn parse(filename: &str) -> Vec<(i64, i64, i64)> {
    let content = std::fs::read_to_string(filename).expect("Provide input to run");
    let mut res = Vec::new();
    for line in content.lines() {
        let items: Vec<&str> = line.split("x").collect();
        if items.len() != 3 {
            panic!(
                "Expected exactly 3 values separated by 'x', but found {}",
                items.len()
            );
        }
        res.push((
            items[0].parse::<i64>().unwrap(),
            items[1].parse::<i64>().unwrap(),
            items[2].parse::<i64>().unwrap(),
        ));
    }
    res
}

fn task1(content: &Vec<(i64, i64, i64)>) -> i64 {
    let mut result = 0;
    for line in content {
        result += 2 * (line.0 * line.1 + line.0 * line.2 + line.1 * line.2);
        result += std::cmp::min(
            line.1 * line.2,
            std::cmp::min(line.0 * line.1, line.0 * line.2),
        );
    }
    result
}

fn task2(content: &Vec<(i64, i64, i64)>) -> i64 {
    let mut result = 0;
    for line in content {
        result += line.0 * line.1 * line.2;
        result += 2 * std::cmp::min(
            line.1 + line.2,
            std::cmp::min(line.0 + line.1, line.0 + line.2),
        );
    }
    result
}

fn main() {
    let content = parse("day02/input");

    let res1 = task1(&content);
    println!("Result 1: {}", res1);

    let res2 = task2(&content);
    println!("Result 2: {}", res2);
}
