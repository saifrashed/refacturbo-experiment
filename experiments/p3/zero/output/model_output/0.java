public static Integer fibonacci(Integer n) {
    if (n <= 1) {
        return n;
    }
    int a = 0;
    int b = 1;
    int fib = 0;

    for (int i = 2; i <= n; i++) {
        fib = a + b;
        a = b;
        b = fib;
    }

    return fib;
}