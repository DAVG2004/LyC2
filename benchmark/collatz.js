function collatzSteps(n) {
    let steps = 0;
    while (n > 1) {
        if (n % 2 === 0) {
            n = n / 2;
        } else {
            n = 3 * n + 1;
        }
        steps++;
    }
    return steps;
}

function main() {
    let maxSteps = 0;
    let bestNum = 0;
    for (let i = 1; i <= 500000; i++) {
        let steps = collatzSteps(i);
        if (steps > maxSteps) {
            maxSteps = steps;
            bestNum = i;
        }
    }
    console.log(`Num: ${bestNum}, Steps: ${maxSteps}`);
}

main();
