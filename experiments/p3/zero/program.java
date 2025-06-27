public class program {
    public static final int INTERNAL_REPETITION_COUNT = 100000;

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();

        for (int x = 0; x < INTERNAL_REPETITION_COUNT; x++) {
            fibonacci(x);
        }

        long endTime = System.currentTimeMillis();
        System.out.println("Execution time: " + (endTime - startTime) / 1000.0 + " seconds");
    }

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
    }}