public class s1 {
    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();

        // Define matrix size
        int n = 2000;
        // Initialize two matrices with random values
        int[][] A = new int[n][n];
        int[][] B = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                A[i][j] = (int) (Math.random() * 100); // Random values 0-99
                B[i][j] = (int) (Math.random() * 100);
            }
        }

        // Perform matrix multiplication
        int[][] result = multiply(A, B);

        long endTime = System.currentTimeMillis();
        System.out.println("Execution time: " + (endTime - startTime) / 1000.0 + " seconds");
    }

    // Matrix multiplication method
    public static int[][] multiply(int[][] A, int[][] B) {
        int n = A.length;
        int[][] result = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    result[i][j] += A[i][k] * B[k][j];
                }
            }
        }
        return result;
    }
}