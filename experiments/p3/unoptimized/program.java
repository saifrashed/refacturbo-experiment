public class program {
    public static final int INTERNAL_REPETITION_COUNT = 500000000;

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();

        for (int x = 0; x < INTERNAL_REPETITION_COUNT; x++) {
            Integer n = Integer.valueOf(40);
            fibonacci(n);
        }

        long endTime = System.currentTimeMillis();
        System.out.println("Execution time: " + (endTime - startTime) / 1000.0 + " seconds");
    }

    public static Integer fibonacci(Integer n) {
        if (n.intValue() <= 1) {
            return Integer.valueOf(n.intValue());
        }
        Integer a = Integer.valueOf(0);
        Integer b = Integer.valueOf(1);
        Integer fib = Integer.valueOf(0);

        for (Integer i = Integer.valueOf(2); i.intValue() <= n.intValue(); i = Integer.valueOf(i.intValue() + 1)) {
            fib = Integer.valueOf(a.intValue() + b.intValue());
            b = fib;
        }
        return fib;
    }
}