public class program {
    public static final int INTERNAL_REPETITION_COUNT = 10000;

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();

        for (int x = 0; x < INTERNAL_REPETITION_COUNT; x++) {
            generateFibonacciString(x);
        }

        long endTime = System.currentTimeMillis();
        System.out.println("Execution time: " + (endTime - startTime) / 1000.0);
    }

    public static String generateFibonacciString(int numRepetitions) {
        StringBuilder result = new StringBuilder();
        int a = 0, b = 1;
        for (int x = 0; x < numRepetitions; x++) {
            result.append(a);
            if (x < numRepetitions - 1) {
                result.append(", ");
            }
            int next = a + b;
            a = b;
            b = next;
        }
        return result.toString();
    }
}