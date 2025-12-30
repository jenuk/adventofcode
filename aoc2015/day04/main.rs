use md5;

fn parse(filename: &str) -> String {
    std::fs::read_to_string(filename)
        .expect("Provide input to run")
        .trim()
        .to_string()
}

fn task1(content: &str) -> i64 {
    let mut counter = 0;
    loop {
        let both: &str = &format!("{}{}", content, counter.to_string());
        let digest = md5::compute(both);
        if digest[0] == 0 && digest[1] == 0 && (digest[2] >> 4) == 0 {
            return counter;
        }
        counter += 1;
    }
}

fn task2(content: &str) -> usize {
    let mut counter = 0;
    loop {
        let both: &str = &format!("{}{}", content, counter.to_string());
        let digest = md5::compute(both);
        if digest[0] == 0 && digest[1] == 0 && digest[2] == 0 {
            return counter;
        }
        counter += 1;
    }
}

fn main() {
    let content = parse("day04/input");

    let res1 = task1(&content);
    println!("Result 1: {}", res1);

    let res2 = task2(&content);
    println!("Result 2: {}", res2);
}
