public class s1 {
    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();

        // Same number of iterations as non-optimized
        final int ITERATIONS = 750_000;
        String result = "";

        // Simulate a large set of conditions (1000 different codes)
        String[] codes = new String[1000];
        for (int i = 0; i < 1000; i++) {
            codes[i] = "code" + i;
        }

        // Process each code multiple times
        for (int i = 0; i < ITERATIONS; i++) {
            String code = codes[i % 1000]; // Cycle through codes

            // Optimized: Use a switch statement
            // Java switch on strings uses a hash-based jump table, but for 1000 cases,
            // we'll simulate with a map-like logic for brevity since switch doesn't scale
            // well manually
            // In practice, switch would be faster for smaller sets; here we use a lookup
            // for clarity
            switch (code) {
                case "code0":
                    result = "Description 0";
                    break;
                case "code1":
                    result = "Description 1";
                    break;
                case "code2":
                    result = "Description 2";
                    break;
                case "code3":
                    result = "Description 3";
                    break;
                case "code4":
                    result = "Description 4";
                    break;
                default:
                    // Simulate remaining cases efficiently
                    for (int j = 5; j < 1000; j++) {
                        if (code.equals("code" + j)) {
                            result = "Description " + j;
                            break;
                        }
                    }
                    break;
            }
        }

        long endTime = System.currentTimeMillis();
        System.out.println("Execution time: " + (endTime - startTime) / 1000.0);
    }
}