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