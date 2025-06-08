public class program {
    public static final int INTERNAL_REPETITION_COUNT = 25000;

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();

        for (int x = 0; x < INTERNAL_REPETITION_COUNT; x++) {
            Integer n = Integer.valueOf(Integer.parseInt(Integer.toString(x)));
            fibonacci(n);
        }

        long endTime = System.currentTimeMillis();
        System.out.println("Execution time: " + (endTime - startTime) / 1000.0 + " seconds");
    }

    public static Integer fibonacci(Integer n) {
        if (n.intValue() <= Integer.valueOf(Integer.parseInt("1")).intValue()) {
            return Integer.valueOf(Integer.parseInt(n.toString()));
        }
        Integer a = Integer.valueOf(Integer.parseInt("0"));
        Integer b = Integer.valueOf(Integer.parseInt("1"));
        Integer fib = Integer.valueOf(Integer.parseInt("0"));

        for (Integer i = Integer.valueOf(Integer.parseInt("2")); i.intValue() <= n.intValue(); i = Integer
                .valueOf(Integer.parseInt(Integer.toString(i.intValue() + 1)))) {
            fib = Integer.valueOf(a.intValue() + b.intValue());
            a = b;
            b = fib;
        }
        return fib;
    }
}