public class program {
    public static final int INTERNAL_REPETITION_COUNT = 500000000;

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();

        for (int x = 0; x < INTERNAL_REPETITION_COUNT; x++) {
            getFibonacci(49);
        }

        long endTime = System
                .currentTimeMillis();
        System.out.println("Execution time: " + (endTime - startTime) / 1000.0 + " seconds");
    }

    static public long getFibonacci(int n) {
        return switch (n) {
            case 0 -> 0;
            case 1 -> 1;
            case 2 -> 1;
            case 3 -> 2;
            case 4 -> 3;
            case 5 -> 5;
            case 6 -> 8;
            case 7 -> 13;
            case 8 -> 21;
            case 9 -> 34;
            case 10 -> 55;
            case 11 -> 89;
            case 12 -> 144;
            case 13 -> 233;
            case 14 -> 377;
            case 15 -> 610;
            case 16 -> 987;
            case 17 -> 1597;
            case 18 -> 2584;
            case 19 -> 4181;
            case 20 -> 6765;
            case 21 -> 10946;
            case 22 -> 17711;
            case 23 -> 28657;
            case 24 -> 46368;
            case 25 -> 75025;
            case 26 -> 121393;
            case 27 -> 196418;
            case 28 -> 317811;
            case 29 -> 514229;
            case 30 -> 832040;
            case 31 -> 1346269;
            case 32 -> 2178309;
            case 33 -> 3524578;
            case 34 -> 5702887;
            case 35 -> 9227465;
            case 36 -> 14930352;
            case 37 -> 24157817;
            case 38 -> 39088169;
            case 39 -> 63245986;
            case 40 -> 102334155;
            case 41 -> 165580141;
            case 42 -> 267914296;
            case 43 -> 433494437;
            case 44 -> 701408733;
            case 45 -> 1134903170;
            case 46 -> 1836311903;
            case 47 -> 2971215073L;
            case 48 -> 4807526976L;
            case 49 -> 7778742049L;
            default -> -1;
        };    }
}