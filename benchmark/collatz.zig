const std = @import("std");

fn collatzSteps(start_n: u64) u32 {
    var n = start_n;
    var steps: u32 = 0;
    while (n > 1) {
        if (n % 2 == 0) {
            n /= 2;
        } else {
            n = n * 3 + 1;
        }
        steps += 1;
    }
    return steps;
}

pub fn main() !void {
    var max_steps: u32 = 0;
    var best_num: u64 = 0;
    var i: u64 = 1;
    while (i <= 500000) : (i += 1) {
        const steps = collatzSteps(i);
        if (steps > max_steps) {
            max_steps = steps;
            best_num = i;
        }
    }
    const stdout = std.io.getStdOut().writer();
    try stdout.print("Num: {}, Steps: {}\n", .{best_num, max_steps});
}
